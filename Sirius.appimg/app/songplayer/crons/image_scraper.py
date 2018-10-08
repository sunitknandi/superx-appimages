from django_cron import CronJobBase, Schedule
from songplayer.models import Artist, Album
from songplayer.util.images_download import googleimagesdownload  # importing the library


class ImageScraper(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "songplayer.wiki"

    def do(self):
        album = Album.objects.all()
        for i in album:
            flag = 0
            artist = Artist.objects.filter(id=i.artist_id.id).first()
            artist_name = artist.artist_name
            album_name = i.album_name
            response = googleimagesdownload()
            arguments = {"keywords": album_name+" " +
                         artist_name, "limit": 1, "print_urls": True}
            paths, url = response.download(arguments)
            i.image = url
            i.save(update_fields=["image"])
