# Inside socassess

It is worth understanding how socassess maps test case outcomes into feedback
messages. For this, I will refer to the sample assessment
[`a1`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/>)
for detailed explanation.

## `maps/__init__.py`

The most essential file is
[`maps/__init__.py`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/maps/__init__.py>).
I'll start with its simple form without enabling email nor AI features. In this
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

The `"selected"` inside `__all__` is required since socassess dynamically
imports the module `maps`---which also means the module/folder name has to be
"maps"---and then it will look for the `selected` dict.

The `selected` dict contains the things to be assessed. You can think of it as
sub-questions for an assignment, or small components of a large component. For
example, you can make it contain `compile` and `execution` like the following,
indicating you want to provide feedback for `compile` and `execution`
separately.

```python
selected = {
    "compile": ...,
    "execution": ...,
}
```

For each key, socassess uses its corresponding dict value to map test case
outcomes into feedback messages. For example, in the above case,
`mapping.single` is for the `single` component, whose content is shown here:

```python
single = {
    frozenset([
        'test_it::test_single::passed',
    ]): {
        'feedback': 'Congrats! test_single passed',
    },
}
```

Given that, socassess will check if the test `test_it::test_single` has passed
or not. If it passed, then the feedback message _Congrats! test_single passed_
will be shown.

If an automated feedback cannot be provided, a default feedback message will be
shown for the relevant component, informing students that there are certain
parts haven't been assessed. For the above case, it will show:

```text
## non_auto

non_auto: automated feedback is not available
```

The default feedback message can be customized in
[`socassess.toml`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/socassess.toml#L21>).
The default template is:

```toml
not_available = "{question}: automated feedback is not available"
```

Where `{question}` will be replaced by the dict key, _i.e._, `non_auto`.

One can code question contents in the `__init__.py` file for quick reference,
such as:

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

questions = {
    "single": "regular 1-to-1 test-feedback mapping",
    "combined": "many-to-1 test-feedback mapping",
    "level": "level-structured feedback mapping",
    "regex": "feedback for parametrized tests using regex",
    "non_auto": "no automated feedback",
    "xxx": "no feedback for this question since it is not selected",
}
```

However, the `questions` dict will not be used by socassess.
