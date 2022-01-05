from django.db import models

from omap.core.dynamic_models import DynamicModel

class DynamicProperties(models.Model):
    additional_properties = models.JSONField(null=True)

    class Meta:
        abstract = True

class ExampleModel(models.Model):
    additional_properties = models.JSONField(null=True)


# class DynamicExample(DynamicModel):
#     id = models.AutoField(primary_key=True)
