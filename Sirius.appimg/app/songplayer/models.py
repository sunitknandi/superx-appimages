from django.db import models


class Genre(models.Model):
    title = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.title
    

class Artist(models.Model):
    artist_name = models.CharField(null=False, max_length=100)
    genre = models.ManyToManyField(Genre)
    artist_image = models.CharField(null=True, max_length=10000)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    album_name = models.CharField(null=False, default='', max_length=100)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.CharField(null=True, max_length=10)
    image = models.CharField(null=True, max_length=100000)

    def __str__(self):
        return self.album_name

class Youtube(models.Model):
    link = models.CharField(null=False, max_length=500)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)


class Song(models.Model):
    name = models.CharField(null=False, max_length=200)
    target = models.FileField(null=True, max_length=10000)
    album_id = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name