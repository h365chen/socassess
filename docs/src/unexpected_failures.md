# Unexpected Failures

Let's consider the following test case used in a first-year programming course
which requires students to write C programs.

```python
def test_mode():
    """Check if the student's program calculates the mode correctly."""
    # Prepare arguments for subprocess
    args = ["./mode", "1", "2", "2", "3", "3"]
    # Run the process
    result = subprocess.run(args, text=True, capture_output=True)
    # Check for abnormal exit conditions
    assert result.returncode == 0 and result.stdout != "", "Program exited abnormally"
    # Verify the output
    lines = result.stdout.splitlines()
    # lines[0] has to contain the output
    ans = list(map(int, lines[0].split()))
    expected_mode = [2, 3]
    assert ans == expected_mode, "Incorrect output"
    # If all assertions pass
    pass
```

Apparently the assessment creator has coded several novice-friendly message to
aid students to interpret the feedback. Ideally, the test case should only fail
in those assertions. However, this code can also fail at the line:

```python
    ans = list(map(int, lines[0].split()))
```

It can fail since the student's program may simply output non-integer
characters, failling the `map(int, ...)`. The feedback, in this case, will be:

```text
ValueError: invalid literal for int() with base 10: 'mode'
```

This is not novice-friendly. Even worse, it has nothing to do with C.

So the point I would like to mention here is that most of the time, what we want
is to ensure the test case to only fail at assertions (or any place that is
expected). If the test case failed at a place outside assertions. This is what I
referred to as an unexpected failure.

## Solution

The solution is actually simple: for any test case that contains non-assertion
code, we code an outcome *flipped* version.

```python
def test_a():
    x = common_code()
    assert x == 0

def test_a_flipped():
    x = common_code()
    assert x != 0
```

If one passed and the other failed, we know they both reached the assertion.
