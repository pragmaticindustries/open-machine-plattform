import logging
from enum import Enum
from inspect import signature

from django import forms
from django.forms import CharField, IntegerField, FloatField


class FieldTypes(Enum):
    TEXT = 1
    INTEGER_NUMBER = 2
    FLOAT_NUMBER = 3


class UserDefinedField:

    def __init__(self, name: str, field_type: FieldTypes, verbose_name: str = None, required: bool = False, **kwargs):
        self.required = required
        self.verbose_name = verbose_name
        self.field_type = field_type
        self.name = name
        self.kwargs = kwargs


def udf_to_forms_field(field: UserDefinedField) -> forms.Field:
    """
    Needs to be extended to handle all types of FieldTypes
    :param field:
    :return:
    """
    if field.field_type == FieldTypes.TEXT:
        field_class = CharField
    elif field.field_type == FieldTypes.INTEGER_NUMBER:
        field_class = IntegerField
    elif field.field_type == FieldTypes.FLOAT_NUMBER:
        field_class = FloatField
    else:
        raise NotImplementedError(f"Type {field.field_type} is not implemented yet!")
    return field_class(required=field.required, **field.kwargs)


class DynamicFieldsMixin(object):
    """
    Mixin to render additional fields to a ModelForm which will be saved in a JSONField.
    Usage:

        class MyForm(DynamicFieldsMixin, forms.ModelForm):
            class Meta:
                model = MyModel
                exclude = ("additional_properties",) # The paramenter where the dynamic fields are stored is not allowed to be rendered
                additional_property_field = "additional_properties" # can be neglected, with this default value
                additional_property_config = [UserDefinedField(name="name", field_type=FieldTypes.TEXT, required=True)]

    This will lead to the generation of a Form, similar to:

        class MyForm(DynamicFieldsMixin, forms.ModelForm):
            name = CharField(required=True)
            class Meta:
                model = MyModel
                exclude = ("additional_properties",)

    which will handle the rendering of initial data as well as saving in the json field.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Add the additional fields here
        if not hasattr(self.__class__, "Meta"):
            raise ValueError("Can only be used on Model Forms with a Meta class!")

        Meta = self.__class__.Meta

        self.add_prop_field = getattr(Meta, "additional_property_field", "additional_properties")

        # Check if the model class has the field
        if not self.add_prop_field in [f.name for f in self._meta.model._meta.get_fields()]:
            raise ValueError("The given 'additional_property_field' is not in the model!")

        self.add_prop_config = getattr(Meta, "additional_property_config", None)

        if not self.add_prop_config:
            raise ValueError("No Config is given, please add 'additional_property_config' in Meta!")

        if self.add_prop_field in self.fields:
            raise ValueError("The field for the additional properties is available as FormField which is not allowed")

        # Add fields
        self.config = self.get_config(kwargs.get("instance", None))

        for field in self.config:
            print(f"Adding dynamic field '{field.name}'")
            self.fields[field.name] = udf_to_forms_field(field)

        # If an instance is given, add initial
        if "instance" in kwargs:
            instance = kwargs["instance"]

            if instance is not None:
                for field in self.config:
                    initial_value = getattr(instance, self.add_prop_field)
                    if field.name in initial_value:
                        self.initial[field.name] = initial_value[field.name]

    def get_config(self, instance=None):
        if type(self.add_prop_config) == list:
            config = self.add_prop_config
        elif callable(self.add_prop_config):
            sig = signature(self.add_prop_config)

            # Check if an unknown parameter exists
            for n, _ in sig.parameters.items():
                if n not in {"model", "instance"}:
                    raise ValueError(f"Unknown Parameter '{n}' in callable function")

            kwargs = {}
            if "model" in sig.parameters:
                kwargs["model"] = self._meta.model
            if "instance" in sig.parameters:
                kwargs["instance"] = instance

            config = self.add_prop_config(**kwargs)

        else:
            raise ValueError("config can either be a name or a callable!")
        return config

    def save(self, commit=True):
        if self.cleaned_data.get(self.add_prop_field):
            raise ValueError("Cannot overwrite value for Dynamic Property Field!")

        additional_properties = {}

        if self.instance:
            stored_properties = getattr(self.instance, self.add_prop_field)
            if stored_properties:
                additional_properties.update(stored_properties)

        for field in self.config:
            value = self.cleaned_data.get(field.name)
            if value:
                additional_properties[field.name] = value

        setattr(self.instance, self.add_prop_field, additional_properties)
        super().save(commit)
