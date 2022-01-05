import uuid

from django.db import models

from omap.core.dynamic_forms import FieldTypes
from omap.core.models.example import DynamicProperties


class HasUUID(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, editable=False, default=uuid.uuid4
    )

    class Meta:
        abstract = True


class HasSemantics(models.Model):
    semantic_identifier = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class AssetType(HasSemantics):
    """
    Assets can be of different types.
    E.g. Machines, Robots, ...
    """
    id = models.UUIDField(
        primary_key=True, null=False, editable=False, default=uuid.uuid4
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Asset(HasSemantics, DynamicProperties):
    identifier = models.CharField(max_length=255)
    asset_type = models.ForeignKey(AssetType, null=True, blank=True, on_delete=models.RESTRICT, related_name="assets")


class RelationType(HasSemantics):
    pass


class AssetRelation(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, editable=False, default=uuid.uuid4
    )

    parent = models.ForeignKey(
        Asset,
        null=False,
        on_delete=models.RESTRICT,
        related_name="children_relations",
    )
    child = models.ForeignKey(
        Asset,
        null=False,
        on_delete=models.RESTRICT,
        related_name="parent_relations",
    )

    relation_type = models.ForeignKey(
        RelationType, null=False, on_delete=models.RESTRICT
    )


class AdditionalField(HasUUID, HasSemantics):
    name = models.CharField(max_length=255)

    data_type = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in FieldTypes]  # Choices is a list of Tuple
    )

    required = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.name} ({FieldTypes(self.data_type).name})"
