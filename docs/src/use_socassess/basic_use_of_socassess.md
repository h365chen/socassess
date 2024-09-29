# Basic Use of socassess

## `maps/__init__.py`

The most essential file is
[`maps/__init__.py`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/maps/__init__.py>).
I'll start with its simple form, not enabling email or AI features. In this
case, the file looks like:

```python
from . import mapping

__all__ = [
    "selected",
]

selected = {
    "single": mapping.single,
    "combined": mapping.combined,
    "level": mapping.level,
    "regex": mapping.regex,
    "non_auto": mapping.non_auto,
}
```

The `"selected"` inside `__all__` is required because socassess dynamically
imports the module _`maps`_—which also means the module/folder name has to be
*maps*—and then it will look for the `selected` dictionary.

The `selected` dictionary contains the items to be assessed. You can think of it
as *questions* for an assignment, or small components of a large component. For
example, you can include `compile` and `execution` as separate components,
indicating you want to provide feedback for `compile` and `execution`
separately.

```python
selected = {
    "compile": ...,
    "execution": ...,
}
```

For each key, socassess uses its corresponding dictionary value to map test case
outcomes into feedback messages. For example, in the above case,
`mapping.single` is for the `single` question. Assume its content is as follows:

```python
# inside mapping.py
single = {
    frozenset([
        'test_it::test_single::passed',
    ]): {
        'feedback': 'Congrats! test_single passed.',
    },
}
```

Given that, socassess will check if the test `test_it::test_single` has passed
or not. If it passed, then the feedback message *Congrats! test_single passed*
will be shown.

```
## single

Congrats! test_single passed.
```

If automated feedback cannot be provided, a default feedback message will be
shown for the relevant question, informing students that certain parts have not
been assessed. For the above case, it will show:

```
## non_auto

non_auto: automated feedback is not available.
```

The default feedback message can be customized in
[`socassess.toml`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/socassess.toml#L21>).
The default template is:

```toml
not_available = "{question}: automated feedback is not available."
```

Where `{question}` will be replaced by the dictionary key, _i.e._, `non_auto`.

In addition to `not_available`, there are a few more configurable items in the
`[template]` table (TOML calls it a
[*table*](<https://toml.io/en/v1.0.0#table>)).

The default feedback template in
[`socassess.toml`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/socassess.toml>)
is:

```toml
[template]
# feedback of one question
one_separator = "\n"  # to join the list of feedback within a question
one = '''
## {question}

{text}
''' # supports two keys: `question` and `text`

# full feedback of all questions
full_separator = "\n"  # to join the list of feedback of all questions
full = '''
# Feedback

{text}''' # supports one key: `text`
not_available = "{question}: automated feedback is not available." # supports one key: `question`
```

socassess assumes there can be multiple maps for a single question.

```python
level = {
    frozenset([
        'test_it::test_level_1::passed',
    ]): {
        'feedback': "Congrats! test_level_1 passed.",
    },
    frozenset([
        'test_it::test_level_2::passed',
    ]): {
        'feedback': "Congrats! test_level_2 passed.",
    },
}
```

In the above example, if the student's program passed both
`test_it::test_level_1` and `test_it::test_level_2`, then both feedback messages
*Congrats! test_level_1 passed.* and *Congrats! test_level_2 passed.* should be
shown. socassess uses `one_separator` to concatenate the two messages to form
`{text}`, then the final message for this one question will be formatted using
`one`, with `{question}` being replaced by `level`. Therefore, the feedback
should look like:

```text
## level

Congrats! test_level_1 passed.
Congrats! test_level_2 passed.

```

If there are multiple questions, for example, if we have questions `single`,
`level`, and `non_auto`, then socassess will use `full_separator` to concatenate
their formatted feedback messages to form `{text}` for `full`:

```text
# Feedback

## single

Congrats! test_single passed.

## level

Congrats! test_level_1 passed.
Congrats! test_level_2 passed.

## non_auto

non_auto: automated feedback is not available.

```

## `FeedbackLevel`

There are times when certain feedback should be given higher priority than
others, even though their underlying test cases do not have dependencies. For
example, if a student's code has a style issue and meanwhile it is not
compilable, and you somehow put the relevant feedback messages in the same
question, in this case, you might just want to provide feedback focusing on the
compilation. Feedback on style issues can be postponed until the student's
program becomes compilable. `FeedbackLevel` is used to control feedback
priorities.

The first case is to control feedback priorities within the same question.

```python
from socassess import FeedbackLevel

level = {
    frozenset([
        'test_it::test_level_lowest::passed',
    ]): {
        'feedback': """
Congrats! test_level_lowest passed. However, this feedback should not be shown.
        """.strip(),
        'level': FeedbackLevel.LOWEST,
    },
    frozenset([
        'test_it::test_level_medium_1::passed',
    ]): {
        'feedback': """
Congrats! test_level_medium_1 passed. This feedback should be shown.
        """.strip(),
        'level': FeedbackLevel.MEDIUM,
    },
    frozenset([
        'test_it::test_level_medium_2::passed',
    ]): {
        'feedback': """
Congrats! test_level_medium_2 passed. This feedback should be shown.
        """.strip(),
        'level': FeedbackLevel.MEDIUM,
    },
}
```

Given the above mapping, if a program passed all `test_it::test_level_lowest`,
`test_it::test_level_medium_1`, and `test_it::test_level_medium_2`, only the
feedback for `test_it::test_level_medium_1` and `test_it::test_level_medium_2`
will be shown because of the higher feedback level:


```text
## level

Congrats! test_level_medium_1 passed. This feedback should be shown.
Congrats! test_level_medium_2 passed. This feedback should be shown.

```

The possible values for `FeedbackLevel` are (See
[level.py](<https://github.com/h365chen/socassess/blob/main/src/socassess/level.py>)):

```python
class FeedbackLevel(IntEnum):
    LOWEST = 10  # default
    LOW = 20
    MEDIUM = 30
    HIGH = 40
    HIGHEST = 50
    # only display this feedback and ignore feedback for all other questions
    SINGLE = 100
```

Since they are `IntEnum`, so using an integer also works, such as:

```python
    {
        'feedback': "...",
        'level': 5,
    }
```

To control feedback priorities across questions, we have to use
`FeedbackLevel.SINGLE`. If a feedback message to be shown is configured at the
level of `FeedbackLevel.SINGLE`, then socassess will only display this feedback
message, regardless of other feedback levels.

```python
level = {
    frozenset([
        'test_it::test_level_single::passed',
    ]): {
        'feedback': """
Congrats! test_level_single passed. Only this feedback will be shown.
        """.strip(),
        'level': FeedbackLevel.SINGLE,  # 100
    },
    frozenset([
        'test_it::test_level_very_high::passed',
    ]): {
        'feedback': """
Congrats! test_level_very_high passed. This feedback should not be shown.
        """.strip(),
        'level': 200,  # higher than FeedbackLevel.SINGLE
    },
}
```

In the above case, assuming the program passed all relevant test cases, the
feedback will be:

```
# Feedback

## _single_feedback_only

Congrats! test_level_single passed. Only this feedback will be shown.

```

The key is hard-coded as `_single_feedback_only`, which might be changed in the
future, but it is what it is for now.

A use case is when the submitted file is incorrectly named
(`test_incorrect_file_name`) or not compilable (`test_compilation`), then it
might lead to lots of `not_available` feedback since test cases for other
questions are likely to be `skipped` and thus socassess cannot find valid
mappings for those questions. In this case, setting the feedback priority for
`test_incorrect_file_name` or `test_compilation` as `FeedbackLevel.SINGLE` is
ideal.

## `artifacts/report.xml`

When invoking socassess, it requires the `--artifacts` to be specified. This
option asks for the user to specify the folder to save generated artifacts.
Usually, I will invoke socassess using:

```bash
socassess feedback --artifacts=artifacts ...
```

In socassess, the provided maps do not access the pytest results directly. The
pytest results are saved into a file called `report.xml` under the specified
artifacts path. Therefore in my case, it will be `artifacts/report.xml`.

The first reason is sometimes I would like to access the intermediate result for
further inspection. The second reason is certain platforms such as GitLab accept
XML files for displaying test results. The third reason is that I don't have to
rerun pytest when I just want to tweak my feedback messages; this is very useful
when a certain test takes a long time and meanwhile you are sure that the result
of it will not change.

For example, assume we are inside the `a1/a1` folder, then the following command
which invokes both pytest and maps:

```bash
socassess feedback \
    --config=socassess.toml \
    --artifacts=artifacts \
    --ansdir=stu \
    --probing=probing_tests --feedback=maps
```

is the same as invoking pytest and maps separately:

```bash
# first command
socassess feedback \
    --config=socassess.toml \
    --artifacts=artifacts \
    --ansdir=stu \
    --probing=probing_tests

# second command
socassess feedback \
    --config=socassess.toml \
    --artifacts=artifacts \
    --ansdir=stu \
    --feedback=maps
```

To tweak my feedback messages, I can invoke the second command multiple times
while the first command only once.

Insofar, a basic introduction to socassess is provided. The next few sections
will discuss more complex use cases.
