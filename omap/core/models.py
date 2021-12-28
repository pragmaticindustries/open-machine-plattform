from django.db import models


class ExampleModel(models.Model):
    additional_properties = models.JSONField(null=True)

