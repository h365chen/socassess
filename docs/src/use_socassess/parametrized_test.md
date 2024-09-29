# Parametrized Tests and Feedback

A common approach to assessing a student's program is _output comparison_. This
involves having several test cases that share the same testing logic, with only
the inputs and expected outputs varying.

I have seen people create tests with the testing logic copy-pasted.
Consequently, they had to maintain that shared piece of code across multiple
tests. If there was a bug in that code, they had to fix it everywhere.

These tests are called _parametrized tests_, and they can be conveniently
created in pytest. The following example is copied from the pytest
[documentation](<https://docs.pytest.org/en/7.1.x/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions>):

```python
# content of test_expectation.py
import pytest

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

The `@parametrize` decorator defines three different `(test_input, expected)`
tuples: `("3+5", 8)`, `("2+4", 6)`, and `("6*9", 42)`. Therefore, there will be
three test cases in total:

```python
def test_eval("3+5", 8):
    assert eval("3+5") == 8

def test_eval("2+4", 6):
    assert eval("2+4") == 6

def test_eval("6*9", 42):
    assert eval("6*9") == 42
```

Apparently, the last test case out of the three will fail.

By default, pytest assigns a _test id_ or a _node id_ in pytest's terminology to
each of the test cases by joining parameters with `-`, resulting in test cases
such as `test_eval[3+5-8]`, `test_eval[2+4-6]`, and `test_eval[6*9-42]`.
However, one can also customize them (see
[here](<https://docs.pytest.org/en/7.1.x/example/parametrize.html#different-options-for-test-ids>)).

The process of mapping outcomes of parametrized tests into feedback messages has
not been thoroughly thought out. The tedious approach is to refer to test IDs.
For example, given the following parametrized tests:

```python
@pytest.mark.parametrize("param", [1, 2])
def test_all_pass(param):
    pass

@pytest.mark.parametrize("param", [1, 2])
def test_not_all_pass(param):
    if param == 1:
        assert 0
```

You can code maps by referring to individual tests such as `test_all_pass[1]`,
`test_all_pass[2]`, `test_not_all_pass[1]`, and `test_not_all_pass[2]`.
Additionally, socassess allows one to use `*` to provide a feedback message
considering multiple parametrized tests. For example:

```python
    frozenset([
        r'test_it::test_all_pass[*]::passed',  # raw string
    ]): {
        'feedback': "Congrats! All tests passed."
    },
    frozenset([
        r'test_it::test_not_all_pass[*]::passed',  # raw string
    ]): {
        'feedback': "Oops! Some tests did not pass. This feedback will be shown only if all of them match 'passed'."
    },
```

Because `test_not_all_pass[1]` does not match the outcome `passed`, the second
feedback will not be shown.

socassess currently only allows `*`, but it is likely to be extended in future
versions.
