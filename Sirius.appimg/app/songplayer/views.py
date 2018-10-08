from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Song, Album, Artist, Genre
from .serializers import SongSerializer, GenreSerializer, AlbumSerializer, ArtistSerializer
from .decorators import validate_search


class ListSongView(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Song.objects.all()
    serializer_class = SongSerializer


class SongDetailsView(generics.RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        try:
            song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongSerializer(song).data)

        except Song.DoesNotExist:
            return Response(
                data={
                    "message": "Song does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListAlbumView(generics.ListAPIView):    
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class AlbumDetailsView(generics.RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Album.objects.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        try:
            album = self.queryset.get(pk=kwargs["pk"])
            return Response(AlbumSerializer(album).data)

        except Album.DoesNotExist:
            return Response(
                data={
                    "message": "Album does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListArtistView(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ArtistDetailsView(generics.RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get(self, request, *args, **kwargs):
        try:
            artist = self.queryset.get(pk=kwargs["pk"])
            return Response(ArtistSerializer(artist).data)

        except Artist.DoesNotExist:
            return Response(
                data={
                    "message": "Artist does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListGenreView(generics.ListAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailsView(generics.RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get(self, request, *args, **kwargs):
        try:
            genre = self.queryset.get(pk=kwargs["pk"])
            return Response(GenreSerializer(genre).data)

        except Genre.DoesNotExist:
            return Response(
                data={
                    "message": "Genre does not exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SearchView(generics.RetrieveAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = SongSerializer

    def get_queryset(self):
        query = self.request.GET.get("search")
        songs = Song.objects.filter(name__icontains=query).all()
        return songs

    @validate_search
    def get(self, request, *args, **kwargs):
        songs = self.get_queryset()
        if songs:
            return Response(SongSerializer(songs, many=True).data)
        else:
            return Response(
                data={
                    "message": "Nothing Found!"
                },
                status=status.HTTP_404_NOT_FOUND
            )
