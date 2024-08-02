"""TODO: auto collect mappings in this folder."""

from socassess import userargs  # noqa: F401

from . import mapping

__all__ = [
    # required
    "selected",

    # needed only if ai feature is enabled, see below
    "context",
]


# ========
# Required
# ========

selected = {
    "single": mapping.single,
    "combined": mapping.combined,
    "level": mapping.level,
    "regex": mapping.regex,
    "non_auto": mapping.non_auto,
}


# =================================
# Needed when AI feature is enabled
# =================================

context = {
    "selected_questions": {
        "non_auto": "",
    },
    "canonicals": {
        "non_auto": "",
    },
    "stu_answers": {
        "non_auto": (userargs.artifacts / 'student_solution.txt').read_text()
    },
}
