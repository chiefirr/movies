from dateutil import parser

from django.db.models import Count, Window, F
from django.db.models.functions import DenseRank
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.views import MultiSerializerViewSet
from movies_api.helpers.context_managers import check_movie_exists, validate_dates
from movies_api.helpers.movie_helpers import make_movies_api_call, build_movie_dict
from movies_api.models import Movie
from movies_api.serializers import MovieBaseSerializer, MoviesTopSerializer
from movies_api.views.filters.movies import MoviesFilter


class MovieViewSet(MultiSerializerViewSet):
    """
    Viewset which allows to add movies by title, retrieve selected movie by ID and scroll top rated movies.
    create: /api/movies/    ['POST', 'GET']
    POST:   creates movie instance from external API
    GET:    shows list of all movies

    top: /api/movies/top/   ['GET']
    required query parameters: 'period_start', 'period_end' in a format: 'day-month-year'
    GET:  Shows top rated movies based on comments ammount.

    """
    http_method_names = ['get', 'post']

    queryset = Movie.objects.all()

    serializers = {
        "default": MovieBaseSerializer,
        "top": MoviesTopSerializer,
    }

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = MoviesFilter

    ordering_fields = ('year', 'country', 'imdb_rating',)

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        if not title:
            raise ValidationError({'error': 'Title field is required.'})

        api_response = make_movies_api_call(title)
        movie_instance = build_movie_dict(api_response.json())

        serializer = self.get_serializer(data=movie_instance)
        serializer.is_valid(raise_exception=True)

        with check_movie_exists():
            serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def top(self, request, *args, **kwargs):
        period_start = request.query_params.get('period_start')
        period_end = request.query_params.get('period_end')

        with validate_dates(period_start, period_end):
            date_start = parser.parse(period_start)
            date_end = parser.parse(period_end)

        top_movies = self.get_queryset() \
            .prefetch_related('comments') \
            .filter(comments__created__range=[date_start, date_end]) \
            .annotate(total_comments=Count('comments'),
                      rank=Window(
                          expression=DenseRank(),
                          order_by=F('total_comments').desc(),
                      ),) \
            .values('id', 'total_comments', 'rank')

        serializer = self.get_serializer(top_movies, many=True)
        return Response(serializer.data)
