"""Contain tests for student solution.

Please refer to ../maps to see how feedback are composed.

"""

import shutil

import pytest


def test_exist(stu_answer):
    assert stu_answer.exists()


@pytest.mark.dependency(depends=['test_exist'])
def test_single(stu_answer_content):
    """Test content only if the solution file exists."""
    assert len(stu_answer_content) > 0


def test_combined_1():
    pass


def test_combined_2():
    pass


def test_level_lowest():
    pass


def test_level_medium_1():
    pass


def test_level_medium_2():
    pass


@pytest.mark.parametrize("param", [1, 2, 3, 4])
def test_regex_all_pass(param):
    pass


@pytest.mark.parametrize("param", [1, 2, 3, 4])
def test_regex_not_all_pass(param):
    if param == 3:
        assert 0


def test_ai(artifacts, stu_answer):
    # put student file into artifacts so that its content can be sent to AI for
    # feedback.
    shutil.copy(stu_answer, artifacts)
    assert 0, "failed due to unknown reason"


def test_email(artifacts, stu_answer):
    """Prepare email attachments.

    SocAssess uses _attachments.txt to determine what to attach in the email.
    Here it sends out the solution file.

    """
    with (artifacts / '_attachments.txt').open('a') as f:
        f.write(stu_answer.name)
    assert 0, "failed due to unknown reason"
