# from django.test import TestCase
# from rest_framework.test import APITestCase
#
# from movies_api.models import Movie
# from movies_api.serializers import MovieBaseSerializer
#
#
# class MovieSerializerTests(TestCase):
#
#     def setUp(self):
#
#         self.movie = Movie.objects.create(imdb_id='1',
#                                           title='Test title',
#                                           year=2019,
#                                           ratings=9.0,
#                                           type='movie',
#                                           )
#
#
#     def test_contains_expected_fields_movie_serializer(self):
#         data = MovieBaseSerializer(instance=self.movie)
#         self.assertCountEqual(data.fields, {'id', 'movie', 'text', 'created'})
