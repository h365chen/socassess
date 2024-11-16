from .level import FeedbackLevel


def extract(onemap: dict):
    """Extract feedback from a test-feedback map.

    Returns
    -------
    feedback: str

    """
    assert 'feedback' in onemap
    level = onemap['level'] if 'level' in onemap else FeedbackLevel.LOWEST
    feedback = onemap['feedback']
    func_with_params = onemap['function'] if 'function' in onemap else None
    if func_with_params is not None:
        feedback = fill_content(feedback, func_with_params)
    return feedback, level


def fill_content(feedback: str, func_with_params) -> str:
    """Fill fields in the feedback message template.

    The number of fields inside the feedback message must match the number of
    key-values returned by the function.

    socassess first escape all `{` and `}` by replacing them into `{{` and
    `}}`, then change back those fields to be filled.

    For example, if the feedback template is "{a} {b} {c} d" and the fields are
    {a=1, b=2} inside the user maps, then the feedback to be filled will be
    "{a} {b} {{c}} d", so that in the end only fields `a` and `b` are filled.

    """
    assert func_with_params is not None
    # escape all `{` and `}`
    feedback = feedback.replace('{', '{{').replace('}', '}}')
    if isinstance(func_with_params, dict):
        func = func_with_params.pop('name')
        params = func_with_params.pop('params')
        user_defined_fields = func(params=params)
        for k in user_defined_fields:
            feedback = feedback.replace(
                f"{{{{{k}}}}}", f"{{{k}}}"
            )
        feedback = feedback.format(**user_defined_fields)
    else:
        # in case there is no params
        func = func_with_params
        user_defined_fields = func()
        for k in user_defined_fields:
            feedback = feedback.replace(
                f"{{{{{k}}}}}", f"{{{k}}}"
            )
        feedback = feedback.format(**user_defined_fields)
    return feedback


def _context(qn, attr):
    """Fetch context given question number (qn) and attribute."""
    if attr is not None and qn in attr:
        attr_context = attr[qn]
    else:
        attr_context = None
    return attr_context


def context(qn, maps):
    """Fetch question, canonical, and student answer contexts.

    All contexts are collected inside the user defined module `maps`.

    """
    ctx = {}
    if "context" in maps.__dict__:
        mapsctx = maps.__dict__["context"]
        for ele in mapsctx:
            _ctx = _context(qn, mapsctx[ele])
            if _ctx is not None:
                ctx |= {
                    ele: _context(qn, mapsctx[ele])
                }
    return ctx
