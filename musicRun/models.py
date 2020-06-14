from django.db import models

# Create your models here.

class Song(models.Model):
    spotify_uri = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    #artists = models.ManyToManyField(related_name="songs")
    artists = models.CharField(max_length=64)
    bpm = models.IntegerField()
    danceability = models.FloatField()
    energy = models.FloatField()
    valence = models.FloatField()
    duration = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} by {self.artists}"

class SpotifyUser(models.Model):
    spotify_id = models.CharField(max_length=64, primary_key=True)
    songs = models.ManyToManyField(Song, blank=True)

