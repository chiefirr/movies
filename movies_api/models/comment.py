from django.db import models

from core.models.abstract_models import TimeStampedModel


class Comment(TimeStampedModel):
    movie = models.ForeignKey('movies_api.Movie',
                              related_name='comments',
                              on_delete=models.CASCADE,
                              )

    text = models.TextField()
