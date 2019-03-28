from django_filters import BaseInFilter, CharFilter
from django_filters.rest_framework import FilterSet

from movies_api.models import Movie


class ActorInFilter(BaseInFilter, CharFilter):
    pass


class MoviesFilter(FilterSet):
    actors = ActorInFilter(lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = {'year': ['exact', 'gte', 'lte'],
                  'rated': ['exact'],
                  'imdb_rating': ['gte', 'lte'],
                  }
