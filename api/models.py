from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class ApiPermissions(models.Model):
    resource_key = models.CharField(max_length=255)
    api_key = models.ForeignKey(ApiKey)
