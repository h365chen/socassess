import pytest


def test_exist(stu_answer):
    assert stu_answer.exists()


@pytest.mark.dependency(depends=['test_exist'])
def test_query():
    assert False


@pytest.mark.dependency(depends=['test_exist'])
def test_query_flipped():
    assert False
