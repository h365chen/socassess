"""Contain necessary information for SocAssess to provide feedback.."""

from . import general

__all__ = [
    # required
    "questions",
    "selected",
]


# ========
# Required
# ========

selected = {
    "general": general.mappings,
}


questions = {
    "general": "this is a general question",
}