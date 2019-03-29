import datetime

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from movies_api.models import Movie


class TestCommentViewSet(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.movie_body_1 = {'imdb_id': 'tt0034583', 'title': 'Casablanca', 'year': '1942', 'rated': 'PG',
                             'released': datetime.date(1942, 3, 29), 'runtime': datetime.timedelta(0, 6120),
                             'genres': ['Drama', 'Romance', 'War'], 'director': 'Michael Curtiz',
                             'writer': ['Julius J. Epstein (screenplay)', 'Philip G. Epstein (screenplay)',
                                        'Howard Koch (screenplay)', 'Murray Burnett (play)', 'Joan Alison (play)'],
                             'actors': ['Humphrey Bogart', 'Ingrid Bergman', 'Paul Henreid', 'Claude Rains'],
                             'plot': 'A cynical nightclub owner protects an old flame and her husband from Nazis in Morocco.',
                             'languages': ['English', 'French', 'German', 'Italian'], 'country': 'USA',
                             'awards': 'Won 3 Oscars. Another 5 wins & 9 nominations.',
                             'poster': 'https://m.media-amazon.com/images/M/MV5BY2IzZGY2YmEtYzljNS00NTM5LTgwMzUtMzM1NjQ4NGI0OTk0XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_SX300.jpg',
                             'ratings': [{'Source': 'Internet Movie Database', 'Value': '8.5/10'},
                                         {'Source': 'Rotten Tomatoes', 'Value': '97%'},
                                         {'Source': 'Metacritic', 'Value': '100/100'}], 'metascore': '100',
                             'imdb_rating': '8.5',
                             'imdb_votes': 468884, 'type': 'movie', 'dvd': datetime.date(2000, 2, 15),
                             'box_office': None,
                             'production': 'Warner Bros. Pictures', 'website': 'https://www.warnerbros.com/casablanca'}

        self.movie_body_2 = {'imdb_id': 'tt0034585', 'title': 'Another Casablanca', 'year': '1942', 'rated': 'PG',
                             'released': datetime.date(1942, 3, 29), 'runtime': datetime.timedelta(0, 6120),
                             'genres': ['Drama', 'Romance', 'War'], 'director': 'Michael Curtiz',
                             'writer': ['Julius J. Epstein (screenplay)', 'Philip G. Epstein (screenplay)',
                                        'Howard Koch (screenplay)', 'Murray Burnett (play)', 'Joan Alison (play)'],
                             'actors': ['Humphrey Bogart', 'Ingrid Bergman', 'Paul Henreid', 'Claude Rains'],
                             'plot': 'A cynical nightclub owner protects an old flame and her husband from Nazis in Morocco.',
                             'languages': ['English', 'French', 'German', 'Italian'], 'country': 'USA',
                             'awards': 'Won 3 Oscars. Another 5 wins & 9 nominations.',
                             'poster': 'https://m.media-amazon.com/images/M/MV5BY2IzZGY2YmEtYzljNS00NTM5LTgwMzUtMzM1NjQ4NGI0OTk0XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_SX300.jpg',
                             'ratings': [{'Source': 'Internet Movie Database', 'Value': '8.5/10'},
                                         {'Source': 'Rotten Tomatoes', 'Value': '97%'},
                                         {'Source': 'Metacritic', 'Value': '100/100'}], 'metascore': '100',
                             'imdb_rating': '8.5',
                             'imdb_votes': 468884, 'type': 'movie', 'dvd': datetime.date(2000, 2, 15),
                             'box_office': None,
                             'production': 'Warner Bros. Pictures', 'website': 'https://www.warnerbros.com/casablanca'}

        self.movie_1 = Movie.objects.create(**self.movie_body_1)
        self.movie_2 = Movie.objects.create(**self.movie_body_2)

    def test_retrieve_movie_object(self):
        response_retrieve = self.client.get(f'/api/movies/{self.movie_1.pk}/')
        response_retrieve_404 = self.client.get(f'/api/comments/-1/')

        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve_404.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_movie_object(self):
        movies_count = Movie.objects.all().count()
        response_retrieve_1 = self.client.post(f'/api/movies/', {"title": "Titanic"})
        self.assertEqual(response_retrieve_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.all().count(), movies_count + 1)

        with self.assertRaises(AssertionError):
            response_retrieve_2 = self.client.post(f'/api/movies/', {"title": "Titanic"})
            self.assertEqual(response_retrieve_2.status_code, status.HTTP_201_CREATED)

        response_retrieve_3 = self.client.post(f'/api/movies/', {"no_title": ""})
        self.assertEqual(response_retrieve_3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_movies(self):
        response_top_1 = self.client.get(f'/api/movies/top/')
        self.assertEqual(response_top_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_top_1.status_code, status.HTTP_400_BAD_REQUEST)

        response_top_2 = self.client.get(f'/api/movies/top/?period_start=bad_date&period_end=bad_date')
        self.assertEqual(response_top_2.status_code, status.HTTP_400_BAD_REQUEST)

        response_top_2 = self.client.get(f'/api/movies/top/?period_start=1-01-2019&period_end=10-01-2019')
        self.assertEqual(response_top_2.status_code, status.HTTP_200_OK)
