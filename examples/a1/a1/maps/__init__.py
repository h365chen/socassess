"""TODO: auto collect mappings in this folder."""

from socassess import userargs  # noqa: F401

from . import mapping

__all__ = [
    # required
    "questions",
    "selected",

    # needed only if ai feature is enabled, see below
    "canonicals",
    "stu_answers",
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


questions = {
    "single": "regular 1-to-1 test-feedback mapping",
    "combined": "many-to-1 test-feedback mapping",
    "level": "level-structured feedback mapping",
    "regex": "feedback for parametrized tests using regex",
    "non_auto": "no automated feedback",
    "xxx": "no feedback for this question since it is not selected",
}

# =================================
# Needed when AI feature is enabled
# =================================

canonicals = {
    # Currently SocAssess assumes you want to provide a canonical answer, along
    # with the question content and the student answer for AI feedback.
    "single": "",
    "combined": "",
    "level": "",
    "non_auto": "blablabla",
}

stu_answers = {
    "single": "",
    "combined": "",
    "level": "",
    "non_auto": (userargs.artifacts / 'student_solution.txt').read_text()
}
