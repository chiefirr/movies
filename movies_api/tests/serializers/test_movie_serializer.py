from django.test import TestCase

from movies_api.models import Movie
from movies_api.serializers import MovieBaseSerializer, MoviesTopSerializer


class MovieSerializerTests(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(imdb_id='1',
                                          title='Test title',
                                          year=2019,
                                          ratings=9.0,
                                          type='movie',
                                          )

        self.top_movie = {"id": 1,
                          "total_comments": 5,
                          "rank": 5,
                          }

    def test_contains_expected_fields_movie_serializer(self):
        data = MovieBaseSerializer(instance=self.movie)
        self.assertCountEqual(data.fields,
                              ('id', 'title', 'year', 'imdb_id', 'rated', 'released', 'runtime', 'genres', 'director',
                               'writer', 'actors', 'plot', 'languages', 'country', 'awards', 'poster',
                               'ratings', 'metascore', 'imdb_rating', 'imdb_votes', 'type', 'dvd',
                               'box_office', 'production', 'website',))

    def test_top_serializer_expected_fields(self):
        data = MoviesTopSerializer(instance=self.top_movie)
        self.assertCountEqual(data.fields, ('id', 'total_comments', 'rank'))
