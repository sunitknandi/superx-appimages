from django_cron import CronJobBase, Schedule
from songplayer.models import Artist
from songplayer.util.images_download import googleimagesdownload


class ArtistImageScraper(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'songplayer.genre'

    def do(self):
        artists = Artist.objects.all()
        for i in artists:
            artist_name = i.artist_name
            response = googleimagesdownload()
            arguments = {"keywords": artist_name +
                         " band", "limit": 1, "print_urls": True}
            paths, url = response.download(arguments)
            i.artist_image = url
            i.save(update_fields=["artist_image"])
