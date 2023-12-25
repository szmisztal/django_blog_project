from django.utils import timezone
from django.db import models


class Entry(models.Model):
    title = models.CharField(max_length = 50, blank = False)
    publication_date = models.DateField(default = timezone.now)
    text = models.TextField(max_length = 1000, blank = False)
