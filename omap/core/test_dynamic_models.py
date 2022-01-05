import pytest
from django.forms import fields_for_model

from omap.core.models import DynamicExample


@pytest.mark.django_db
def test_dynamic_model():
    fields = fields_for_model(DynamicExample)
    assert len(fields) == 0

    instance = DynamicExample()
    instance.save()

    assert len(instance._meta.concrete_fields) == 2
