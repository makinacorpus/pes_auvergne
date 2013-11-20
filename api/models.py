# encoding: utf-8

from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class ApiPermissions(models.Model):
    object_type = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    api_key = models.ForeignKey(ApiKey)
