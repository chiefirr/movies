import requests
from contextlib import contextmanager

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from movies_api.exceptions import MoviesAPIError


@contextmanager
def check_response():
    """
    Context manager for checking connection with external API
    """
    try:
        yield
    except requests.exceptions.RequestException:
        raise MoviesAPIError({"error": "Can't connect with external API."})


@contextmanager
def check_movie_exists():
    """
    Context manager for checking if movie has not been already created
    """
    try:
        yield
    except IntegrityError:
        raise MoviesAPIError({"error": "This film already exists."})


@contextmanager
def validate_dates(period_start, period_end):
    """
    Validates dates from query params.
    :param period_start: start date, date format
    :param period_end: end date, date format
    """
    if not (period_start or period_end):
        raise ValidationError({"error": "You should provide both 'period_start and 'period_end' parameters"})

    try:
        yield
    except ValueError:
        raise ValidationError({"error": "Bad date format! Try: 'day-month-year'"})
