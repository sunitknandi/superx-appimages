from django.urls import path
from .views import ListSongView, SongDetailsView, ListAlbumView, AlbumDetailsView, ListArtistView,\
    ArtistDetailsView, ListGenreView, GenreDetailsView, SearchView


urlpatterns = [
    path('songs/', ListSongView.as_view(), name="songs-all"),
    path('songs/<int:pk>/', SongDetailsView.as_view(), name="songs-detail"),
    path('albums/', ListAlbumView.as_view(), name="albums-all"),
    path('albums/<int:pk>/', AlbumDetailsView.as_view(), name="albums-detail"),
    path('artists/', ListArtistView.as_view(), name="artists-all"),
    path('artists/<int:pk>/', ArtistDetailsView.as_view(), name="artists-detail"),
    path('genres/', ListGenreView.as_view(), name="genres-all"),
    path('genres/<int:pk>/', GenreDetailsView.as_view(), name="genres-detail"),
    path('search/', SearchView.as_view(), name="search"),
]
