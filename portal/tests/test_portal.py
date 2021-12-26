import pytest

from omap.assets.models import SimpleAsset


@pytest.mark.django_db
def test_simple():
    assert SimpleAsset.objects.count() == 0
