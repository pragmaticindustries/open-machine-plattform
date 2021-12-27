import uuid

from django.db import models


class BaseAsset(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, editable=False, default=uuid.uuid4
    )
    identifier = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        abstract = True


class SimpleAsset(BaseAsset):
    pass


class RelationType(models.Model):
    pass


class AssetRelation(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, editable=False, default=uuid.uuid4
    )

    parent = models.ForeignKey(
        SimpleAsset,
        null=False,
        on_delete=models.RESTRICT,
        related_name="children_relations",
    )
    child = models.ForeignKey(
        SimpleAsset,
        null=False,
        on_delete=models.RESTRICT,
        related_name="parent_relations",
    )

    relation_type = models.ForeignKey(
        RelationType, null=False, on_delete=models.RESTRICT
    )
