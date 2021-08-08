from django.db import models


class Song(models.Model):
    url = models.URLField()
    song_id = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    #

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
