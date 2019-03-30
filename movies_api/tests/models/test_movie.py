from django.test import TestCase

from movies_api.models import Movie


class MovieModelTests(TestCase):

    def test_should_return_name(self):
        movie = Movie(title="Test title", year=2000)
        assert movie.__str__() == "Test title (2000)"
