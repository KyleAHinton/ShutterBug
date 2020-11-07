from django.db import models
from django.conf import settings

class Image (models.Model):
    url = models.CharField(max_length=2048, blank=False, default='')
    mods = models.JSONField(default=dict)

class Portfolio (models.Model):
    photo = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.JSONField(default=list)
    
    class Meta:
        unique_together = (("photo", "user"))