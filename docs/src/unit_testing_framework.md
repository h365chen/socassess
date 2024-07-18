# Unit Testing Framework

A weird misunderstanding of automated assessments is that people think it is
trivial to create them. However, my experience tells me that it is in fact a
difficult task.

The first time when I created an automated assessment to grade students'
programs, I wrote almost everything from sratch, because I thought it might just
be few lines of code to compare the output from the student's program against
the expected output. However, soon I realized that what I needed to write was
not just the lines to compare the outputs. Additionally, I had to write bunch of
code to properly iterate students' programs, clean up any intermediate results
and side effect, and collect grades and feedback. All those things had
distracted me a lot.

Further, I also realized that the assessment code should be organized flexibly.
For instance, if an assignment contained two questions in a previous course
offering, and you created assessment code to assess both questions, but later
you decided to split the assignment into two smaller assignments with each
contains only one question. In that case, you want your assessment code can be
conveniently re-constructed.

I'll demonstrate how I managed to use the unit testing framework
[pytest](<https://docs.pytest.org/en/stable/contents.html>) to handle these
problems.

## pytest

I'm sure there are more things to discuss if the complexity of the assessment
code is high, but here are several essential concepts about pytest that allowed
me to write my assessment code efficiently. In particular, they are _test
discovery_, _fixture_, _fixture scope_, and _teardown/cleanup_.

### Test Discovery ([see its pytest doc](<https://docs.pytest.org/en/stable/explanation/goodpractices.html#conventions-for-python-test-discovery>))

In our case, we just need to remember that pytest implements the standard Python
test discovery. That means it will search for `test_*.py` or `*_test.py` files,
and in those file, it will collect `test` prefixed functions or methods outside
of class, and `test` prefixed functions or methods inside `Test` prefixed
classes (without an `__init__` method).

For example, given the following folder structure and code in the files

```bash
tests
├── a.py
└── test_a.py
```

```python
# a.py

def test_a():
    assert True
```

```python
# test_a.py

def test_a():
    assert True


class A:
    def test_a(self):
        assert True


class TestA:
    def test_a(self):
        assert True
```

Then the results of `pytest -v tests` will be since `a.py` and class `A` are
skipped.

```bash
tests/test_a.py::test_a PASSED
tests/test_a.py::TestA::test_a PASSED
```

### Fixtures ([see its pytest doc](<https://docs.pytest.org/en/stable/explanation/fixtures.html#about-fixtures>))

> In testing, a fixture provides a defined, reliable and consistent context for
> the tests. This could include environment (for example a database configured
> with known parameters) or content (such as a dataset).

pytest knows a particular function to be a fixture if it is decorated with
`@pytest.fixture`. There can be more than one fixture for a test. Fixtures can
use (or depend on) other fixtures. If an earlier fixture has a problem and
raises an exception, pytest will stop executing fixtures for that test and mark
the test as having an error, which means the test could not be attempted.

A fixture often returns something which can be later used in test functions. In
the following example, the `my_obj` argument in the `test_obj` function is the
object returned by the `my_obj` fixture.

```python
import pytest


@pytest.fixture
def my_obj():
    return "Assume this is an object"


def test_obj(my_obj):
    assert my_obj == "Assume this is an object"
```

pytest has lots of useful built-in fixtures (see
[its list](<https://docs.pytest.org/en/stable/reference/fixtures.html>)). Here are
some of them which I think are very useful.

- [`capsys`/`capfd`](<https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html#accessing-captured-output-from-a-test-function>):
  it allows you to access captured output from a test function without caring
  about setting/resetting output streams.
- [`tmp_path`](<https://docs.pytest.org/en/stable/how-to/tmp_path.html#the-tmp-path-fixture>):
  it provides a temporary directory unique to each test function.
- [`request`](<https://docs.pytest.org/en/stable/reference/reference.html#std-fixture-request>):
  it provides information for the requesting test function, see an example
  [here](<https://docs.pytest.org/en/stable/example/simple.html#request-example>).


### Fixture Scope ([see its pytest doc](<https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes>))

By default, fixtures have the scope of `function`, which means fixtures are
destroyed at the end of the test.
