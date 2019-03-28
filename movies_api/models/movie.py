import datetime

from django.contrib.postgres import fields
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Movie(models.Model):
    # GENERAL = 'General Audiences'
    # PARENTAL_SUGGESTED = 'Parental Guidance Suggested'
    # PARENTS_CAUTIONED = 'Parents Strongly Cautioned'
    # RESTRICRED = 'Restricted'
    # ADULTS_ONLY = 'Adults Only'
    #
    # AGE_RESTRICTIONS = (
    #     (GENERAL, 'G'),
    #     (PARENTAL_SUGGESTED, 'PG'),
    #     (PARENTS_CAUTIONED, 'PG-13'),
    #     (RESTRICRED, 'R'),
    #     (ADULTS_ONLY, 'NC-17'),
    # )

    class Meta:
        unique_together = ('imdb_id', 'title',)

    imdb_id = models.CharField(max_length=32)

    title = models.CharField(max_length=128,
                             db_index=True,
                             )

    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1895), max_value_current_year])

    rated = models.CharField(max_length=16,
                             null=True,
                             )

    released = models.DateField(null=True)

    runtime = models.DurationField(null=True)

    genres = fields.ArrayField(models.CharField(max_length=128),
                               null=True,
                               )

    director = models.CharField(max_length=128,
                                null=True,
                                )

    writer = fields.ArrayField(models.CharField(max_length=128),
                               null=True)

    actors = fields.ArrayField(models.CharField(max_length=128),
                               null=True)

    plot = models.TextField(null=True)

    languages = fields.ArrayField(models.CharField(max_length=64),
                                  null=True,
                                  )

    country = models.CharField(max_length=128,
                               null=True,
                               )

    awards = models.TextField(null=True)

    poster = models.URLField(null=True)

    ratings = fields.JSONField()

    metascore = models.PositiveSmallIntegerField(null=True)

    imdb_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                    null=True)

    imdb_votes = models.IntegerField(null=True)

    type = models.CharField(max_length=64)

    dvd = models.DateField(null=True)

    box_office = models.IntegerField(null=True)

    production = models.CharField(max_length=128,
                                  null=True,
                                  )

    website = models.URLField(null=True)

    def __str__(self):
        return f'{self.title} ({self.year})'
