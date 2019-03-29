from unittest import TestCase

import pytest
import datetime
from dateutil import parser
from collections import namedtuple

class ExceptionTestCase(TestCase):
    ERRORS = {
        "bad_input": "Bad input.",
        "server_error": "Ooops! Looks like we have broken external API! :) Try another title.",
        "does_not_exist": "Looks like film with this title does not exist.",
    }

    def test_check_status(self):
        from movies_api.helpers.movie_helpers import _check_status
        Response = namedtuple('Response', ['status_code', 'json'])

        def json_true():
            return {"Response": "True"}

        def json_false():
            return {"Response": "False"}

        response_200 = Response(200, json_false)
        response_400 = Response(400, json_true)
        response_404 = Response(404, json_true)
        response_500 = Response(500, json_true)

        from movies_api.exceptions import MoviesAPIError
        with self.assertRaises(MoviesAPIError) as context:
            _check_status(response_200)
        self.assertEqual(context.exception.message['error'], self.ERRORS["does_not_exist"])

        with self.assertRaises(MoviesAPIError) as context2:
            _check_status(response_400)
        self.assertEqual(context2.exception.message['error'], self.ERRORS["bad_input"])

        with self.assertRaises(MoviesAPIError) as context3:
            _check_status(response_404)
        self.assertEqual(context3.exception.message['error'], self.ERRORS["bad_input"])

        with self.assertRaises(MoviesAPIError) as context4:
            _check_status(response_500)
        self.assertEqual(context4.exception.message['error'], self.ERRORS["server_error"])


def test_build_movie_dict():
    from movies_api.helpers.movie_helpers import build_movie_dict
    raw_data = {'Title': 'Casablanca', 'Year': '1942', 'Rated': 'PG', 'Released': '23 Jan 1943', 'Runtime': '102 min',
                'Genre': 'Drama, Romance, War', 'Director': 'Michael Curtiz',
                'Writer': 'Julius J. Epstein (screenplay), Philip G. Epstein (screenplay), Howard Koch (screenplay), Murray Burnett (play), Joan Alison (play)',
                'Actors': 'Humphrey Bogart, Ingrid Bergman, Paul Henreid, Claude Rains',
                'Plot': 'A cynical nightclub owner protects an old flame and her husband from Nazis in Morocco.',
                'Language': 'English, French, German, Italian', 'Country': 'USA',
                'Awards': 'Won 3 Oscars. Another 5 wins & 9 nominations.',
                'Poster': 'https://m.media-amazon.com/images/M/MV5BY2IzZGY2YmEtYzljNS00NTM5LTgwMzUtMzM1NjQ4NGI0OTk0XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_SX300.jpg',
                'Ratings': [{'Source': 'Internet Movie Database', 'Value': '8.5/10'},
                            {'Source': 'Rotten Tomatoes', 'Value': '97%'},
                            {'Source': 'Metacritic', 'Value': '100/100'}], 'Metascore': '100', 'imdbRating': '8.5',
                'imdbVotes': '468,884', 'imdbID': 'tt0034583', 'Type': 'movie', 'DVD': '15 Feb 2000',
                'BoxOffice': 'N/A', 'Production': 'Warner Bros. Pictures',
                'Website': 'https://www.warnerbros.com/casablanca', 'Response': 'True'}

    test_dict = {'imdb_id': 'tt0034583', 'title': 'Casablanca', 'year': '1942', 'rated': 'PG',
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
                             {'Source': 'Metacritic', 'Value': '100/100'}], 'metascore': '100', 'imdb_rating': '8.5',
                 'imdb_votes': 468884, 'type': 'movie', 'dvd': datetime.date(2000, 2, 15), 'box_office': None,
                 'production': 'Warner Bros. Pictures', 'website': 'https://www.warnerbros.com/casablanca'}
    assert build_movie_dict(raw_data) == test_dict


def test_replace_na():
    from movies_api.helpers.movie_helpers import _replace_na
    test_dict = {"one": "one", "two": "N/A"}
    _replace_na(test_dict)
    assert test_dict["one"] == "one"
    assert test_dict["two"] == None


def test_movie_duration():
    from movies_api.helpers.movie_helpers import _movie_duration
    assert _movie_duration("150 minutes") == datetime.timedelta(minutes=150)
    assert _movie_duration(None) == None


def test_parse_date():
    from movies_api.helpers.movie_helpers import _parse_date
    movie_release_date = "19 Dec 1997"
    assert _parse_date(movie_release_date) == parser.parse(movie_release_date).date()
    assert _parse_date(None) == None


def test_parse_str_into_list():
    from movies_api.helpers.movie_helpers import _parse_str_into_list
    test_data = "Test one, Test two, Test three"
    assert _parse_str_into_list(test_data) == ["Test one", "Test two", "Test three"]
    assert _parse_str_into_list(None) == None


def test_parse_votes():
    from movies_api.helpers.movie_helpers import _parse_votes
    assert _parse_votes("941,210") == 941210
    assert _parse_votes(None) == None


def test_parse_boxoffice():
    from movies_api.helpers.movie_helpers import _parse_boxoffice
    assert _parse_boxoffice("$226,276,809") == 226276809
