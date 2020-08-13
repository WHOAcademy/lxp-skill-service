from django.db import models
from django.conf import settings


class SkillModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_seconds = models.IntegerField()
    creation_date = models.DateTimeField()
    last_mod_date = models.DateTimeField()

    def __str__(self):
        return self.title
