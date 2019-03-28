import datetime

from django.test import TestCase
from rest_framework.test import APITestCase

from movies_api.models import Movie, Comment
from movies_api.serializers import CommentBaseSerializer


class CommentSerializerTests(TestCase):

    def setUp(self):

        self.movie = Movie.objects.create(imdb_id='1',
                                          title='Test title',
                                          year=2019,
                                          ratings=9.0,
                                          type='movie',
                                          )

        self.comment = Comment.objects.create(movie=self.movie,
                                              text="Some test text",
                                              created=datetime.date.today()
                                              )


    def test_contains_expected_fields_comment_serializer(self):
        data = CommentBaseSerializer(instance=self.comment)
        self.assertCountEqual(data.fields, {'id', 'movie', 'text', 'created'})
