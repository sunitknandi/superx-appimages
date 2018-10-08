from django_cron import CronJobBase, Schedule
from config import Secrets
from django.conf import settings
from songplayer.models import Song, Artist, Album, Genre
import os
from mutagen.easyid3 import EasyID3


class SongInfo(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'songplayer.songinfo'

    def do(self):
        path = os.path.abspath(Secrets.SONG_DIRECTORY)
        files = os.listdir(path)
        for file in files:
            try:
                print(file)
                song = EasyID3(path+"/"+file)
                response = song
                genre, _ = Genre.objects.get_or_create(
                    title=response["genre"][0].title())
                artist_obj = self.get_artist_id(response['artist'][0], genre)
                album_obj, _ = Album.objects.get_or_create(
                    album_name=response['album'][0], date=response["date"][0][0:4], artist_id=artist_obj)
                _, _ = Song.objects.get_or_create(name=response['title'][0], target=self.upload_file_path(
                    response['title'][0], file), album_id=album_obj)

            except Exception as e:
                print(e)

    @staticmethod
    def get_artist_id(artist_name, genre):
        artist_obj = Artist.objects.filter(artist_name=artist_name).first()

        if not artist_obj:
            artist_obj = Artist.objects.create(artist_name=artist_name)
            artist_obj.genre.add(genre)
            return artist_obj
        artist_obj.genre.add(genre)
        return artist_obj

    @staticmethod
    def upload_file_path(title, file):
        path = os.path.abspath(Secrets.SONG_DIRECTORY)
        media_path = os.path.abspath(settings.MEDIA_ROOT)
        os.rename(path+"/"+file, media_path+"/audio/" +
                  ("_".join(title.split())+".mp3"))
        return "audio/{name}".format(name=("_".join(title.split()))+".mp3")
