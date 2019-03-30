from django.db import models

from core.models.abstract_models import TimeStampedModel


class Comment(TimeStampedModel):
    movie = models.ForeignKey('movies_api.Movie',
                              related_name='comments',
                              on_delete=models.CASCADE,
                              )

    text = models.TextField()

    def __str__(self):
        return f'Comment {self.pk}: to movie {self.movie}'
