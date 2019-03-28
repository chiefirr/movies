from django_filters.rest_framework import FilterSet

from movies_api.models import Comment


class CommentsFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {'movie': ['exact'],
                  }
