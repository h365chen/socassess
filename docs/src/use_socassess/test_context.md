# Using Test Context in Feedback

To provide detailed feedback based on test outcomes, there needs to be a
mechanism for maps to utilize the test context. For instance, if
`test_compilation` fails, including the raw compilation error message in the
feedback can guide students to correct their code.

Assuming `--artifacts=artifacts` is specified when invoking socassess, by
default, only the `artifacts/report.xml` will be generated. However, the
`artifacts` folder can be used as the bridge for maps to access test context.

Consider this example with a test named `test_and_provide_context`, which has a
parameter called `artifacts`:

```python
from pathlib import Path

def test_and_provide_context(artifacts: Path):
    ...
```

Here, `artifacts` is a fixture defined in `conftest.py`, with the implementation
as follows:

```python
# inside conftest.py
@pytest.fixture(scope="session")
def artifacts(request) -> Path:
    """Contains the folder path to store artifacts."""
    opt = request.config.getoption("--artifacts")
    return Path(opt)
```

This setup allows storing any desired test context that maps might later access,
such as:

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

When the test `test_and_provide_context` runs, it creates a file named
`test_case_context.txt` containing several log lines.

socassess permits access to the artifacts folder through `userargs.artifacts`.
Here shows an example:

```python
from socassess import userargs

detail = {
    frozenset([
        'test_it::test_and_provide_context::passed',
    ]): {
        'feedback': """
Congrats! test_and_provide_context passed.

In addition, here are more details about it:

{content}
        """.strip(),
        'function': (userargs.artifacts / 'test_case_context.txt').read_text,
    },
}
```

Note the new key `function`. The value of `function` must be a
[callable](<https://docs.python.org/3/glossary.html#term-callable>); hence, in
the example, it is `.read_text` instead of `.read_text()`.

Upon encountering such a callable, socassess will execute it and use its result
to fill `{content}`. Therefore, the automated feedback will be:

```
## detail

Congrats! test_and_provide_context passed.

In addition, here are more details about it:

test_and_provide_context: log line #1
test_and_provide_context: log line #2
test_and_provide_context: log line #3
test_and_provide_context: log line ...
```

## Using a Function with Parameters

It is feasible to use the same function in multiple places with only minor
differences. In such cases, a `params` parameter can be provided to the
function, requiring it to be defined as `def func(params)`. This approach is
particularly useful when the function itself is complex. Here is an example:

```python
# test cases (always pass)
# note that we assume they are executed sequentially
# so it is fine for them to append text to the same file

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

with

```python
{
    'feedback': ...,
    'function': { 'name': myfunc, 'params': myparams },
    ...
}
```

The `params` can be any type, such as a `str`, a `list`, or a `dict`. Here we
define `def shared_func(params)` with `params` assigned to
`test_and_provide_context_1` or `test_and_provide_context_2` separately.

```python
# maps

from socassess import userargs

def shared_func(params: str):
    content = (userargs.artifacts / 'test_case_context.txt').open('r')
    filtered_lines = []
    for line in content:
        if params in line:
            filtered_lines.append(line)
    return f"""
{params} passed.

In addition, here are more details about it:

{''.join(filtered_lines)}
    """.strip()

detail = {
    frozenset([
        'test_it::test_and_provide_context_1::passed',
    ]): {
        'feedback': "Congrats! {content}",
        'function': {
            'name': shared_func,
            'params': 'test_and_provide_context_1',
        }
    },
    frozenset([
        'test_it::test_and_provide_context_2::passed',
    ]): {
        'feedback': "Congrats! {content}",
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

In addition, here are more details about it:

test_and_provide_context_1: log line #1
test_and_provide_context_1: log line #2
test_and_provide_context_1: log line #3
test_and_provide_context_1: log line ...
Congrats! test_and_provide_context_2 passed.

In addition, here are more details about it:

test_and_provide_context_2: log line #1
test_and_provide_context_2: log line #2
test_and_provide_context_2: log line #3
test_and_provide_context_2: log line ...
```
