from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def expected_filename() -> str:
    """Return the expected file name of the solution file."""
    return 'student_solution.txt'


@pytest.fixture(scope="session")
def assessment_dir(pytestconfig) -> Path:
    """Contains the path to the expected assessment folder."""
    return pytestconfig.rootdir / '..' / 'a1'


@pytest.fixture(scope="session")
def feedback_dir(pytestconfig) -> Path:
    """Contains the folder path to recorded feedback."""
    return pytestconfig.rootdir / 'data' / 'recorded_feedback'


def pytest_generate_tests(metafunc):
    """Parametrize `one_answer` for `cproc`.

    The parametrization can be dynamically done. We look into
    `tests/data/representative_answers` for representative answers.

    """
    if "one_answer" in metafunc.fixturenames:
        # Use the files_list fixture to get the list of files
        rootdir = metafunc.config.rootdir
        answerdir = Path(rootdir / 'data' / 'representative_answers')
        files = list(answerdir.iterdir())
        # one_answer is a full path, so we use `one_answer.name` to get only
        # the file name, e.g., 1.sql, 2.sql, etc.
        metafunc.parametrize(
            "one_answer",
            [
                pytest.param(one_answer, id=one_answer.name)
                for one_answer in files
            ]
        )
