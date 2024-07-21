# Feedback

Recall the target of socassess is to

1. Give automated feedback only on solutions that were previously considered;
1. Otherwise, seek human feedback.

Previously we only talked about how to enhance our assessment code, but we
haven't talked about how to seek human feedback when there is an unexpected
solution.

The idea is that: instead of coding a feedback message for each test case, we
code feedback messages for test case sets. Here is a simple example showing
assessing a SQL query with some details omitted.

These are some relevant test cases.

```python
def test_exist(stu_answer):
    assert stu_answer.exists()


@pytest.mark.dependency(depends=['test_exist'])
def test_query():
    # ... omitted
    pass


@pytest.mark.dependency(depends=['test_exist'])
def test_query_flipped():
    # ... omitted
    pass
```

These are the feedback messages. Notice that I will also code some complimentary
feedback messages since I believe they are very helpful in motivating students
to learn.

```python
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
```

## Human Feedback

Given the above pre-coded feedback messages, is it possible that the test case
outcomes do not fall into any of them? Apparently it is a yes. For example, both
`test_query` and `test_query_flipped` can fail at the same time due to, say,
database connection issues. These feedback messages have not covered that
situation.

When there is no automated feedback message can be provided, socassess will seek
human feedback. Currently, it can send emails to instructors, where the content
can be customized (see
[`socassess.toml`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/socassess.toml>)).
