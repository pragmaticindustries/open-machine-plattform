from django.contrib import admin

from omap.core.models.assets import AssetType, RelationType, AssetRelation, AdditionalField, Asset

admin.site.register(AssetType)
admin.site.register(Asset)
admin.site.register(RelationType)
admin.site.register(AssetRelation)
admin.site.register(AdditionalField)
