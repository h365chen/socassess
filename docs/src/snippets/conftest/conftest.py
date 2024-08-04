import random

import pytest


@pytest.fixture(scope="module")
def module_val():
    """Generate a random number."""
    return random.randint(0, 9)


@pytest.fixture(scope="session")
def session_val():
    """Generate a random number."""
    return random.randint(0, 9)
