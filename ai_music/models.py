from django.db import models


class Music(models.Model):
    midi_file = models.FileField(upload_to='midi_files/')
