from django.db import models

class URL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_url} -> {self.long_url}"
