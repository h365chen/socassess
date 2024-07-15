# Unexpected Failures

Let's consider the following test case used in a first-year programming course.

```python
def test_mode():
    """Check if the student's program calculates the mode correctly."""
    # Prepare arguments for subprocess
    args = ["./Mode", "1", "2", "2", "3", "3"]
    # Run the process
    result = subprocess.run(args, text=True, capture_output=True)
    # Check for abnormal exit conditions
    assert result.returncode == 0 and result.stdout != "", "Program exited abnormally"
    # Check if there is a segmentation fault
    assert result.returncode != -11, "Segfault!"
    # Verify the output
    lines = result.stdout.splitlines()
    # lines[0] has to contain the output
    ans = list(map(int, lines[0].split()))
    expected_mode = [2, 3]
    assert ans == expected_mode, "Incorrect output"
    # If all assertions pass
    print("passed")
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

This is not novice-friendly.
