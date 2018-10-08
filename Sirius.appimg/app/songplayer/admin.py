from django.contrib import admin
from .models import Artist, Genre, Album, Song


admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Song)
