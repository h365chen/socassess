"""Allow communication between pytest and user maps."""

from pathlib import Path

# flake8: noqa
artifacts: Path = None  # will be initialized in main()
pytest_context: dict = {}
