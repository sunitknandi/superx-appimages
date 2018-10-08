from rest_framework import serializers
from .models import Song, Album, Artist, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("__all__")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'artist_name', 'genre', 'artist_image')


class AlbumSerializer(serializers.ModelSerializer):
    artist_id = ArtistSerializer()

    class Meta:
        model = Album
        fields = ('id', 'album_name', 'artist_id', 'image')


class SongSerializer(serializers.ModelSerializer):
    album_id = AlbumSerializer()

    class Meta:
        model = Song
        fields = ('id', 'name', 'target', 'album_id')
