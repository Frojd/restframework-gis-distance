from django.db import models
from django.contrib.gis.db.models import PointField


class Record(models.Model):
    location = PointField()

    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
