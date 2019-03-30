import datetime

from django.test import TestCase

from movies_api.models import Comment, Movie


class CommentModelTests(TestCase):
    movie_dict = {'imdb_id': 'tt0034583', 'title': 'Casablanca', 'year': 1942, 'rated': 'PG',
                  'released': datetime.date(1943, 1, 23), 'runtime': datetime.timedelta(0, 6120),
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
                              {'Source': 'Metacritic', 'Value': '100/100'}], 'metascore': '100', 'imdb_rating': '8.5',
                  'imdb_votes': 468884, 'type': 'movie', 'dvd': datetime.date(2000, 2, 15), 'box_office': None,
                  'production': 'Warner Bros. Pictures', 'website': 'https://www.warnerbros.com/casablanca'}

    def test_should_return_comment_name(self):
        movie = Movie.objects.create(**self.movie_dict)
        comment = Comment(movie=movie, pk=5)
        assert comment.__str__() == f"Comment 5: to movie {movie}"
