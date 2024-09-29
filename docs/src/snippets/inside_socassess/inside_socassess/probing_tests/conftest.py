from pathlib import Path

import pytest


def pytest_addoption(parser):
    """Add necessary pytest configurations."""
    parser.addoption(
        "--artifacts", action="store", default="artifacts"
    )
    parser.addoption(
        "--ansdir", action="store", default="stu"
    )


@pytest.fixture(scope="session")
def artifacts(request) -> Path:
    """Contains the folder path to store artifacts."""
    opt = request.config.getoption("--artifacts")
    return Path(opt)


@pytest.fixture(scope="session")
def stu_answer(request) -> Path:
    """Contains the folder path containing student's solution file."""
    opt = request.config.getoption("--ansdir")
    return Path(opt) / 'student.txt'


@pytest.fixture(scope="session")
def stu_answer_content(stu_answer) -> Path:
    """Read and return the content of the student answer file."""
    return stu_answer.read_text()
