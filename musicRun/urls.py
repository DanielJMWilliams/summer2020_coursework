from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generate", views.generate, name="generate"),
    path("callback", views.callback, name="callback"),
    path("createRunningPlaylist", views.createRunningPlaylist, name="createRunningPlaylist"),
    path("playlists", views.playlists, name="playlists"),
    path("importPlaylist", views.importPlaylist, name="importPlaylist"),
    path("playlist/<str:playlist_id>", views.playlist, name="playlist"),
    path("importedSongs", views.importedSongs, name="importedSongs"),
    path("importLikedSongs/<int:offset>", views.importLikedSongs, name="importLikedSongs"),
    path("profile", views.profile, name="profile"),
    path("spotify_logout", views.spotify_logout, name="spotify_logout"),
]