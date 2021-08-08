from django.db import models


class Song(models.Model):
    STATUS = (("NA", "N/A"), ("downloading", "downloading"), ("success", "success"), ("fail", "fail"))
    url = models.URLField()
    song_id = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS, default="NA")
    file = models.FileField(null=True)
    #

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
