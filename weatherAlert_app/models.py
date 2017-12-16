from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(max_length=64)
    webhook = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=64, default='USA')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.city

@python_2_unicode_compatible
class Owner(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    email = models.EmailField(null=True)
    is_active = models.BooleanField(default=True)

    @property
    def slack_handle(self):
        return '@{}'.format(''.join(self.email[0:len(self.email)-13]))

    def __str__(self):
        return self.name