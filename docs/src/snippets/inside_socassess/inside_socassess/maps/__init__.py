"""Contain necessary information for SocAssess to provide feedback.."""

from socassess import userargs  # noqa: F401

from . import mapping

__all__ = [
    "selected",
]


selected = {
    "detail": mapping.detail,
}
