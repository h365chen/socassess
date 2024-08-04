import pytest


@pytest.fixture
def my_obj():
    return "Assume this is an object"


def test_obj(my_obj):
    assert my_obj == "Assume this is an object"
