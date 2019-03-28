from rest_framework import serializers

from movies_api.models import Comment


class CommentBaseSerializer(serializers.ModelSerializer):
    """Base comment serializer"""
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'text', 'created', )

        read_only_fields = ('id', 'created',)
