# Unexpected Failures

Let's consider the following test case used in a first-year programming course
that requires students to write C programs.

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

The assessment creator has coded several novice-friendly messages to aid
students in interpreting the feedback. Ideally, the test case should only fail
at those assertions. However, this code can also fail at the line:

```python
    ans = list(map(int, lines[0].split()))
```

This failure can occur because the student's program may output non-integer
characters, causing the `map(int, ...)` to fail. The resulting feedback would
be:

```text
ValueError: invalid literal for int() with base 10: 'mode'
```

This feedback is not novice-friendly and, even worse, it is unrelated to C
programming.

The point I want to make here is that most of the time, we want the test case to
fail only at assertions or at any place that is expected. If the test case fails
outside of assertions, this is what I refer to as an *unexpected failure*.

## Solution

The solution is actually quite simple: for any test case that contains
non-assertion code, we code an outcome *flipped* version.

```python
def test_a():
    x = common_code()
    assert x == 0

def test_a_flipped():
    x = common_code()
    assert x != 0
```

If one passes and the other fails, we know they both reached the assertion. This
strategy helps ensure that the test cases fail only for the intended reasons.
