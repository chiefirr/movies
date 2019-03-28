from rest_framework import serializers

from movies_api.models import Movie


class MovieBaseSerializer(serializers.ModelSerializer):
    """Base Movie serializer to be used in a ViewSet"""

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'imdb_id', 'rated', 'released', 'runtime', 'genres', 'director',
                  'writer', 'actors', 'plot', 'languages', 'country', 'awards', 'poster',
                  'ratings', 'metascore', 'imdb_rating', 'imdb_votes', 'type', 'dvd',
                  'box_office', 'production', 'website',
                  )

        read_only_fields = ('id',)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MoviesTopSerializer(serializers.ModelSerializer):
    """Serializer to show top rated movies based on comments amount"""

    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ('id', 'total_comments', 'rank')
