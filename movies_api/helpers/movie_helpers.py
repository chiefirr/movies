import datetime

import requests
from dateutil import parser
from rest_framework.exceptions import ValidationError

from movies.settings import API_URL, API_KEY
from movies_api.exceptions import MoviesAPIError
from movies_api.helpers.context_managers import check_response


def build_movie_dict(movie: dict):
    """
    Builds movie dict from json
    :param movie: raw json data from external API response
    :return: movie dict object
    """
    _replace_na(movie)

    movie_dict = dict(
        imdb_id=movie.get('imdbID'),
        title=movie.get('Title'),
        year=_parse_year(movie.get('Year')),
        rated=movie.get('Rated'),
        released=_parse_date(movie.get('Released')),
        runtime=_movie_duration(movie.get('Runtime')),
        genres=_parse_str_into_list(movie.get('Genre')),
        director=movie.get('Director'),
        writer=_parse_str_into_list(movie.get('Writer')),
        actors=_parse_str_into_list(movie.get('Actors')),
        plot=movie.get('Plot'),
        languages=_parse_str_into_list(movie.get('Language')),
        country=movie.get('Country'),
        awards=movie.get('Awards'),
        poster=movie.get('Poster'),
        ratings=movie.get('Ratings'),
        metascore=movie.get('Metascore'),
        imdb_rating=movie.get('imdbRating'),
        imdb_votes=_parse_votes(movie.get('imdbVotes')),
        type=movie.get('Type'),
        dvd=_parse_date(movie.get('DVD')),
        box_office=_parse_boxoffice(movie.get('BoxOffice')),
        production=movie.get('Production'),
        website=movie.get('Website'),
    )
    return movie_dict


def _replace_na(movie: dict):
    """
    Replaces N/A data for None
    :param movie: dict
    :return: None
    """
    for k, v in movie.items():
        if v == 'N/A':
            movie[k] = None


def make_movies_api_call(title: str):
    """
    Calls external API (defined in Settings) with provided API Key.
    :param title: film title,
    :return: API response object
    """
    url_encoded_title = requests.utils.requote_uri(title)
    api_url = f'{API_URL}{API_KEY}&t={url_encoded_title}'
    with check_response():
        api_request = requests.get(api_url)
    _check_status(api_request)
    return api_request


def _check_status(response):
    """
    Checks response status and validates if film with requested title has been found in external API database.
    :param response:
    :return: None
    """
    ERRORS = {
        "bad_input": "Bad input.",
        "server_error": "Ooops! Looks like we have broken external API! :) Try another title.",
        "does_not_exist": "Looks like film with this title does not exist.",
    }

    if 400 <= response.status_code < 500:
        raise MoviesAPIError({"error": ERRORS["bad_input"]})

    elif 500 <= response.status_code < 600:
        raise MoviesAPIError({"error": ERRORS["server_error"]})

    result = response.json()
    if result.get('Response', 'False') == 'False':
        raise MoviesAPIError({"error": ERRORS["does_not_exist"]})


def _parse_year(year):
    """Year parser"""
    try:
        return int(year.split('–')[0])
    except (ValueError, AttributeError):
        raise ValidationError({"error": "This movie has bad release date format. You can't save it."})


def _parse_date(movie_release):
    """Date parser"""
    if movie_release:
        release = parser.parse(movie_release)
        return release.date()


def _movie_duration(duration_str):
    """Duration formatter"""
    if duration_str:
        duration_int = int(duration_str.split(' ')[0])
        duration = datetime.timedelta(minutes=duration_int)
        return duration


def _parse_str_into_list(data_str):
    """List data formatter to be saved into ArrayField"""
    if data_str:
        items = data_str.split(',')
        items_cleaned = [data.lstrip(' ') for data in items]
        return items_cleaned


def _parse_votes(votes_str):
    """Votes parser"""
    if votes_str:
        votes = int(votes_str.replace(',', ''))
        return votes


def _parse_boxoffice(boxoffice_str):
    """Box office parser"""
    if boxoffice_str:
        boxoffice = int(boxoffice_str.lstrip('$').replace(',', ''))
        return boxoffice
