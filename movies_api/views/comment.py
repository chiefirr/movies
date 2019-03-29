from django_filters.rest_framework import DjangoFilterBackend

from core.views import MultiSerializerViewSet
from movies_api.models import Comment
from movies_api.serializers import CommentBaseSerializer
from movies_api.views.filters import CommentsFilter


class CommentViewSet(MultiSerializerViewSet):
    """
    Viewset for adding and listing comments
    """

    http_method_names = ['get', 'post']

    queryset = Comment.objects.all()

    serializers = {
        "default": CommentBaseSerializer,
    }

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CommentsFilter
