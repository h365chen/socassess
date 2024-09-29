# Feedback

Recall that the goal of socassess is to:

1. Give automated feedback only on solutions that were previously considered;
1. Otherwise, seek human feedback.

Previously, we discussed enhancing our assessment code, but we have not yet
addressed how to seek human feedback for unexpected solutions.

The idea is to code feedback messages for sets of test cases rather than
individual cases. Here is a simplified example of assessing a SQL query with
some details omitted.

Here are some relevant test cases:

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

Here are the feedback messages[^1]. Note that I will also include some
complimentary feedback messages, as I believe they are very helpful in
motivating students to learn:

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
        'feedback': 'Oops! Your query returns incorrect results. Remember, you can always contact the instructor team if you have spent too much time figuring it out on your own.'
    },
```

## Human Feedback

Given the above pre-coded feedback messages, is it possible for the test case
outcomes to fall outside these categories? Yes, for instance, both `test_query`
and `test_query_flipped` might fail simultaneously due to a database connection
issue, a scenario not covered by the existing feedback messages.

When no automated feedback can be provided, socassess will seek human feedback.
Currently, it can send emails to instructors, with customizable content.

---

[^1]: In feedback messages, `fronzenset` has to be used since socassess needs it
to be hashable. (See [more info about set and
fronzenset](<https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset>))
