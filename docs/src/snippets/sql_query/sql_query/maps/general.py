mappings = {
    frozenset([
        'test_it::test_exist::failed',
    ]): {
        'feedback': 'Oops! Have you named the file correctly?',
    },
    frozenset([
        'test_it::test_query::passed',
    ]): {
        'feedback': 'Nice! Your query returns correct results.'
    },
    frozenset([
        'test_it::test_query::failed',
        'test_it::test_query_flipped::passed',
    ]): {
        'feedback': 'Oops! Your query returns incorrect results. Remember you can always contact the instructor team if you have spent too much time figuring it out on your own.'
    },
}
