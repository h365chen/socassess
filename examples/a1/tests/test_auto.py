"""Test automated feedback generation."""

import shlex
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def cproc(one_answer: Path,
          expected_filename,
          assessment_dir,
          tmp_path) -> tuple[str, str, str]:
    """Invoke CLI without typing it manually.

    The scope of this fixture should be 'function' since we deal with one
    answer at a time.

    `one_answer` is parametrized dynamically, see conftest.py.

    """
    cwd = Path.cwd()  # get current dir
    # copy the file to avoid modifying the original one by accident
    print('processing: ', one_answer.relative_to(cwd))
    (tmp_path / 'stu').mkdir()
    shutil.copyfile(one_answer, tmp_path / 'stu' / expected_filename)
    # similarly, use a temp folder for artifacts since we do not care about
    # them in these tests
    artifacts = tmp_path / 'artifacts'
    # refer to that file for assessment
    stu = tmp_path / 'stu'
    probing_tests = Path(assessment_dir / 'probing_tests').relative_to(cwd)
    feedback = Path(assessment_dir / 'maps').relative_to(cwd)
    toml = Path(assessment_dir / 'socassess.toml').relative_to(cwd)
    cmd = f"""
socassess feedback
    --artifacts={artifacts}
    --ansdir={stu}
    --config={toml}
    --probing={probing_tests}
    --feedback={feedback}
    """.strip()  # noqa: E501
    print(cmd)
    complete_proc = subprocess.run(shlex.split(cmd),
                                   capture_output=True,
                                   text=True)
    return one_answer.name, complete_proc.stdout, complete_proc.stderr


def test_match(cproc: tuple[str, str, str],
               feedback_dir: Path,
               pytestconfig,
               datarecorder):
    fname, feedback, error_msg = cproc
    # record it as a markdown file
    record_file = feedback_dir / (fname.removesuffix('.sql') + '.md')
    feedback = feedback.replace('---', '')
    datarecorder.record_data(
        recording_type='txt',
        recording_file=record_file,
        data=f"""

# Representative answer

{fname}

# Feedback

```
{feedback}
```

# Error message if any

{error_msg}
        """.strip(),
    )
