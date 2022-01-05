from django import forms
from django.http import HttpResponse
from django.views.generic import CreateView

from omap.core.dynamic_forms import DynamicFieldsMixin, UserDefinedField, FieldTypes
from omap.core.models.assets import Asset


def demo(request):
    return HttpResponse("Hallo")


def hook(model, instance):
    from omap.core.models.assets import AdditionalField
    additional_fields = AdditionalField.objects.all()

    if model == Asset:
        return [
            UserDefinedField(name=field.name, field_type=FieldTypes(field.data_type), required=field.required)
            for field in additional_fields
        ]
    else:
        return []


class AssetForm(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = Asset
        exclude = ("additional_properties",)
        additional_property_config = hook


class AddAsset(CreateView):
    form_class = AssetForm
    model = Asset
    template_name = "omap/core/asset_form.html"

    def get_success_url(self):
        return ""
