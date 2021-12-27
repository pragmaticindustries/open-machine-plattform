from django.contrib import admin

from omap.assets.models import SimpleAsset, RelationType, AssetRelation

admin.site.register(SimpleAsset)
admin.site.register(RelationType)
admin.site.register(AssetRelation)
