import pytest
from django import forms
from django.forms import EmailInput

from omap.core.dynamic_forms import DynamicFieldsMixin, UserDefinedField, FieldTypes
from omap.core.models import ExampleModel


class FormWithDefaultPropertiesName(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        # additional_property_field = "additional_properties"
        additional_property_config = [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]


class FormWithExplicitPropertiesName(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        additional_property_field = "additional_properties"
        additional_property_config = [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]


class FormWithCallableConfig(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        additional_property_field = "additional_properties"

        @staticmethod
        def get_config(model):
            return [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]

        additional_property_config = get_config


class FormWithWidget(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        additional_property_field = "additional_properties"
        additional_property_config = [
            UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=False, widget=forms.EmailInput())]


class FormWithAllTypes(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        additional_property_field = "additional_properties"
        additional_property_config = [
            UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=False),
            UserDefinedField(name="age", field_type=FieldTypes.INTEGER_NUMBER, required=False),
            UserDefinedField(name="pi", field_type=FieldTypes.FLOAT_NUMBER, required=False),
        ]


class WrongFormWithPropertiesField(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        fields = "__all__"
        additional_property_config = [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]


class WrongFormWithNotExisting(DynamicFieldsMixin, forms.ModelForm):
    class Meta:
        model = ExampleModel
        exclude = ("additional_properties",)
        additional_property_field = "not_existing"
        additional_property_config = [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]


valid_forms = [FormWithDefaultPropertiesName, FormWithExplicitPropertiesName, FormWithCallableConfig, FormWithWidget]
invalid_forms = [WrongFormWithPropertiesField, WrongFormWithNotExisting]


@pytest.mark.parametrize("form_class", valid_forms)
@pytest.mark.django_db
def test_dynamic_forms(form_class):
    my_form = form_class(data={"name": "Julian"})
    assert my_form.is_valid()
    my_form.save()
    instance = my_form.instance

    properties = instance.additional_properties

    assert properties == {"name": "Julian"}


@pytest.mark.django_db
def test_empty_fields():
    my_form = FormWithAllTypes(data={"name": "Julian"})
    assert my_form.is_valid()
    my_form.save()
    instance = my_form.instance

    properties = instance.additional_properties

    assert properties == {"name": "Julian"}


@pytest.mark.django_db
def test_all_types():
    my_form = FormWithAllTypes(data={"name": "Julian", "age": "101", "pi": "3.141"})
    assert my_form.is_valid()
    my_form.save()
    instance = my_form.instance

    properties = instance.additional_properties

    assert properties == {"name": "Julian", "age": 101, "pi": 3.141}


@pytest.mark.parametrize("form_class", valid_forms)
@pytest.mark.django_db
def test_change_existing_object(form_class):
    instance = ExampleModel(additional_properties={"age": "101"})
    my_form = form_class(data={"name": "Julian"}, instance=instance)
    my_form.is_valid()
    my_form.save()

    properties = instance.additional_properties
    assert "name" in properties
    assert "age" in properties


@pytest.mark.parametrize("form_class", valid_forms)
@pytest.mark.django_db
def test_show_initial_value(form_class):
    instance = ExampleModel(additional_properties={"name": "Julian"})
    instance.save()
    my_form = form_class(instance=instance)

    assert "name" in my_form.initial
    assert 'value="Julian"' in str(my_form)


@pytest.mark.parametrize("form_class", invalid_forms)
@pytest.mark.django_db
def test_invalid_form(form_class):
    with pytest.raises(ValueError):
        my_form = form_class(data={"name": "Julian"})
        my_form.is_valid()
        my_form.save()


@pytest.mark.django_db
def test_form_with_widget():
    form = FormWithWidget()

    assert isinstance(form.fields["name"].widget, EmailInput)
    assert '<input type="email"' in str(form)
