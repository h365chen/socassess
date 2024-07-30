# Parametrized Test and Feedback

One common approach to assess a student's program is _output comparison_. What
it means is that several test cases share the same testing logic, with only
inputs and expected outputs to be varied.

I have seen people created tests with the testing logic copy-pasted.
Consequently, they had to maintain that shared piece of code across multiple
tests. If there is a bug inside that code, they had to fix it everywhere.

These tests are called _parametrized test_ and they can be created conveniently
in pytest. The following example is copy-pasted from the pytest
[doc](<https://docs.pytest.org/en/7.1.x/how-to/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions>).

```python
# content of test_expectation.py
import pytest


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

The `@parametrize` decorator defines three different `(test_input,expected)`
tuples with `("3+5", 8)`, `("2+4", 6)`, and `("6*9", 42)` respectively.
Therefore, there will be three test cases in total:

```python
def test_eval("3+5", 8):
    assert eval("3+5") == 8

def test_eval("2+4", 6):
    assert eval("2+4") == 6

def test_eval("6*9", 42):
    assert eval("6*9") == 42
```

Apparently, the last test case out of the three will fail.

By default, pytest assigns a _test id_ to each of the test cases by joining
parameters with `-`, thereby aforementioned test cases will be
`test_eval[3+5-8]`, `test_eval[2+4-6]`, and `test_eval[6*9-42]`. However, one
can also customize them (see
[here](<https://docs.pytest.org/en/7.1.x/example/parametrize.html#different-options-for-test-ids>)).

Mapping outcomes of parametrized tests into feedback messages has not been
thoroughly thought out. The tedious approach is to refer to test ids. For
example, given the following parametrized tests:

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
`test_all_pass[2]`, `test_not_all_pass[3]`, and/or `test_not_all_pass[4]`. In
addition, socassess allows one to use `*` to provide a feedback message
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

Because `test_not_all_pass[1]` does not match the outcome `passed`, therefore,
the second feedback will not be shown.

socassess currently only allows `*`, but it is likely to be extended in future
versions.
