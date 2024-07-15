import subprocess

def test_mode():
    """Check if the student's program calculates the mode correctly."""
    # Prepare arguments for subprocess
    args = ["./mode", "1", "2", "2", "3", "3"]
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

