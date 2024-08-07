# Displaying Raw Test Case Outcomes

Being able to obtain raw test case outcomes often aids in the development of
automated assessments. There are several approaches to obtain this information.

## `pytest` Command

`socassess` invokes `pytest` to obtain test case outcomes internally, using a
set of pre-defined `pytest` command-line flags. Currently, `socassess` invokes
`pytest` as follows:

```bash
pytest \
    --junitxml=/path/to/artifacts_dir/report.xml \
    --artifacts=/path/to/artifacts_dir \
    --ansdir=/path/to/submission_dir \
    /path/to/test_dir
```

However, `pytest` accepts much more flexible command-line flags, such as
selecting tests by keyword expressions (`-k`), node ids (`pytest
test_mod.py::test_func`), or marker expressions (`-m`) (See [the complete pytest
command-line
flags](<https://docs.pytest.org/en/7.1.x/reference/reference.html#command-line-flags>)).
Therefore, I would recommend invoking `pytest` through the command line while
developing test cases.

## `socassess` with `--probing` but without `--feedback`

Another approach is to invoke `socassess` with `--probing` but without
`--feedback`, such as:

```bash
socassess feedback \
    --config=socassess.toml \
    --artifacts=artifacts \
    --ansdir=stu \
    --probing=probing_tests
```

In this case, `socassess` will invoke `pytest` using the following command-line
flags and send the output to the console.

```bash
pytest \
    --junitxml=/path/to/artifacts_dir/report.xml \
    -v \
    --tb=line \
    --artifacts=/path/to/artifacts_dir \
    --ansdir=/path/to/submission_dir \
    /path/to/test_dir
```

_Note: When invoking `socassess` with `--probing`, the artifacts folder will be
re-created._

## Setting `raw_feedback = true` in `socassess.toml`

The last approach is preliminary, which is to set `raw_feedback` to `true` in
the `socassess.toml`, such as:

```toml
[feature]
ai = false
email = false
raw_feedback = true
```

This approach allows you to see test summary information from `pytest` alongside
feedback messages. If you set this in the `socassess.toml` of `a1`, running
`socassess` will yield:

```
# Feedback

## single

Congrats! test_single passed

## combined

Congrats! test_combined_1 and test_combined_2 passed

## level

Congrats! test_level_medium_1 passed. This feedback should be shown.
Congrats! test_level_medium_2 passed. This feedback should be shown.

## regex

Congrats! All test_regex tests passed.

## non_auto

non_auto: automated feedback is not available

## _raw_feedback_out_of_testcases

assert 0
AssertionError: failed due to unknown reason
assert 0
AssertionError: failed due to unknown reason
assert 0
```
