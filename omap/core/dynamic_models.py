from django.db import models
from django.db.models.fields import CharField
from django.db.models.base import ModelBase


class DynamicModelMetaclass(ModelBase):

    def __new__(cls, name, bases, attrs, **kwargs):
        clazz = super().__new__(cls, name, bases, attrs, **kwargs)
        field = CharField(name="Hallo")
        clazz.add_to_class("test", field)
#        clazz._meta.private_fields = [field]
        return clazz


class DynamicModel(models.Model, metaclass=DynamicModelMetaclass):

    additional_properties = models.JSONField(null=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
