# Use Test Context in Feedback

In order to provide fine detail of a test, there needs to be a way for maps to
use the context of the test. For example, when `test_compilation` fails, the
feedback might include the raw compilation error message to guide students to
fix the code.

Assume we specify `--artifacts=artifacts` when invoking socassess, by default,
only the `artifacts/report.xml` will be generated. However, the `artifacts`
folder can be used as the bridge for maps to access test context.

In the following example, we have a test called `test_and_provide_context`. It
has a parameter `artifacts`.

```python
from pathlib import Path


def test_and_provide_context(artifacts: Path):
    ...
```

The `artifacts` is a fixture defined in `conftest.py`, whose implementation is
as follows:

```python
# inside conftest.py
@pytest.fixture(scope="session")
def artifacts(request) -> Path:
    """Contains the folder path to store artifacts."""
    opt = request.config.getoption("--artifacts")
    return Path(opt)
```

Therefore, we can use it to store any test context that we would like maps to
access later, such as:

```python
from pathlib import Path


def test_and_provide_context(artifacts: Path):
    (artifacts / 'test_case_context.txt').write_text("""

test_and_provide_context: log line #1
test_and_provide_context: log line #2
test_and_provide_context: log line #3
test_and_provide_context: log line ...

    """.strip())
    assert True
```

Here when the test `test_and_provide_context` executes, it will create a file
called `test_case_context.txt` and put some lines in it.

socassess allows maps to access the artifacts folder by using
`userargs.artifacts`. Here shows an example:

```python
from socassess import userargs

detail = {
    frozenset([
        'test_it::test_and_provide_context::passed',
    ]): {
        'feedback': """
Congrats! test_and_provide_context passed.

In addition, here are more detail of it:

{content}
        """.strip(),
        'function': (userargs.artifacts / 'test_case_context.txt').read_text,
    },
}
```

Notice that there is a new key `function`. The value of `function` has to be a
[callable](<https://docs.python.org/3/glossary.html#term-callable>); thereby in
the above example it is `.read_text` instead of `.read_text()`.

When seeing such a callable, socassess will try to call it. Then socassess will
use its result to fill `{content}` (if there's any). Therefore, for the above
case, the automated feedback will be:

```text
## detail

Congrats! test_and_provide_context passed.

In addition, here are more detail of it:

test_and_provide_context: log line #1
test_and_provide_context: log line #2
test_and_provide_context: log line #3
test_and_provide_context: log line ...
```

## Use function with params

It is possible that the same function being used at multiple places, with only
few differences. Then we can provide a `params` parameter to the function.
However, it requires the function to be coded in the form `def func(params)`. It
is generally useful when the function itself is complex. Here is an example:

```python
# test cases (always pass)
# note that we assume they are executed sequentially
# so it is ok for them to append text to the same file

from pathlib import Path


def test_and_provide_context_1(artifacts: Path):
    f = (artifacts / 'test_case_context.txt').open('a')
    f.write("test_and_provide_context_1: log line #1\n")
    f.write("test_and_provide_context_1: log line #2\n")
    f.write("test_and_provide_context_1: log line #3\n")
    f.write("test_and_provide_context_1: log line ...\n")
    assert True


def test_and_provide_context_2(artifacts: Path):
    f = (artifacts / 'test_case_context.txt').open('a')
    f.write("test_and_provide_context_2: log line #1\n")
    f.write("test_and_provide_context_2: log line #2\n")
    f.write("test_and_provide_context_2: log line #3\n")
    f.write("test_and_provide_context_2: log line ...\n")
    assert True
```

The essential change is to replace

```python
{
    'feedback': ...,
    'function': myfunc,
    ...
}
```

To

```python
{
    'feedback': ...,
    'function': { 'name': myfunc, 'params': myparams },
    ...
}
```

The `params` can be anything you like, such as a `str`, a `list`, a `dict`, and
so on. Here we have `def shared_func(params)` with `params` assigned to
`test_and_provide_context_1` or `test_and_provide_context_2` for different
cases.

```python
# maps

from socassess import userargs


def shared_func(params: str):
    content = (userargs.artifacts / 'test_case_context.txt').open('r')
    # filter out the lines which contain `params`
    filtered_lines = []
    for line in content:
        if params in line:
            filtered_lines.append(line)
    return ''.join(filtered_lines)


detail = {
    frozenset([
        'test_it::test_and_provide_context_1::passed',
    ]): {
        'feedback': """
Congrats! test_and_provide_context_1 passed.

In addition, here are more detail of it:

{content}
        """.strip(),
        'function': {
            'name': shared_func,
            'params': 'test_and_provide_context_1',
        }
    },
    frozenset([
        'test_it::test_and_provide_context_2::passed',
    ]): {
        'feedback': """
Congrats! test_and_provide_context_2 passed.

In addition, here are more detail of it:

{content}
        """.strip(),
        'function': {
            'name': shared_func,
            'params': 'test_and_provide_context_2',
        }
    },
}
```

The feedback will be:

```text
## detail

Congrats! test_and_provide_context_1 passed.

In addition, here are more detail of it:

test_and_provide_context_1: log line #1
test_and_provide_context_1: log line #2
test_and_provide_context_1: log line #3
test_and_provide_context_1: log line ...

Congrats! test_and_provide_context_2 passed.

In addition, here are more detail of it:

test_and_provide_context_2: log line #1
test_and_provide_context_2: log line #2
test_and_provide_context_2: log line #3
test_and_provide_context_2: log line ...
```
