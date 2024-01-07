from socassess import FeedbackLevel

single = {
    # This is the simply case with one feedback for one probing test
    frozenset([
        'test_it::test_single::passed',
    ]): {
        'feedback': 'Congrats! test_single passed',
    },
}

combined = {
    # This is the case where we want to provide a single feedback for multiple
    # probing tests
    frozenset([
        'test_it::test_combined_1::passed',
        'test_it::test_combined_2::passed',
    ]): {
        'feedback': 'Congrats! test_combined_1 and test_combined_2 passed',
    },
}

level = {
    # This is the case where the probing tests are not considered having
    # dependencies, but we want to provide feedback focusing on some of them.
    frozenset([
        'test_it::test_level_lowest::passed',
    ]): {
        'feedback': """
Congrats! test_level_lowest passed. However, this feedback should not be shown.
        """.strip(),
        'level': FeedbackLevel.LOWEST,
    },
    frozenset([
        'test_it::test_level_medium_1::passed',
    ]): {
        'feedback': """
Congrats! test_level_medium_1 passed. This feedback should be shown.
        """.strip(),
        'level': FeedbackLevel.MEDIUM,
    },
    frozenset([
        'test_it::test_level_medium_2::passed',
    ]): {
        'feedback': """
Congrats! test_level_medium_2 passed. This feedback should be shown.
        """.strip(),
        'level': FeedbackLevel.MEDIUM,
    },
}

non_auto = {
    # This is the case where automated feedback cannot be provided. This is an
    # empty dict since we always seek human feedback for this `non_auto`
    # question.
}
