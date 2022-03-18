import pytest


def test_that_does_nothing():
    assert True


@pytest.mark.django_db
def test_that_does_nothing_but_runs_django():
    assert True
