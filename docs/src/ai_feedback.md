# Seek AI Feedback through ChatGPT

AI feedback is configured by following keys in the `socassess.toml`:

```toml
[feature]
ai = true

[openai]
openai_key = "<key>, if empty, use OPENAI_KEY environment variable"
model = "gpt-3.5-turbo"
temperature = 1
max_tokens = 2048
top_p = 1
frequency_penalty = 0
presence_penalty = 0
system_prompt = """\
You are an expert in assessing students' answers. Your message will be sent \
directly to students. When the instructor provides you with a student's answer, \
you will give a short feedback message to correct student's misunderstanding, \
but without leaking any infomation of the canonical or correct answer directly. \
       """  # per TOML spec, in "" string, "\" will be used to trim whitespaces and newlines
template = '''
AI generated feedback:
{feedback}'''  # support one key: `feedback`; AI response will replace {feedback}
textwrap_width = 80
```

Most of them are passed to the OpenAI python client
([openai-python](<https://github.com/openai/openai-python>)) transparently,
thereby you can refer to OpenAI's API
[here](<https://platform.openai.com/docs/api-reference/chat/create>) for
explanation on them. The two exceptions are the `template` and `textwrap_width`
key, which specifies how socassess displays the AI feedback and with what
maximum column width (unlimited if `textwrap_width` does not exist).

Given the above configuration, a sample feedback might be:

```
AI generated feedback:
Great start! Make sure to review the question prompt carefully and ensure that
your answer file aligns with all the requirements. Keep up the good work!
```

## Question Context

<div class="warning">

Currently, this is only used for AI feedback; however, I would like to extend
the email feature to use it as well in the future.

</div>

By default, socassess sends nothing to ChatGPT seeking feedback, therefore, it
is likely that ChatGPT will make a reply such as: *Please provide me with the
student's answer that you would like me to assess.*

That said, in order to receive a valid AI feedback, you have to provide some
context, such as the student answer for the question. In the following example,
I provided the student answer for the `non_auto` question.

```python
# maps/__init__.py

from socassess import userargs
~
~from . import mapping
~
~__all__ = [
~    # required
~    "selected",
~
~    # needed only if ai feature is enabled, see below
~    "context",
~]
~
~
~# ========
~# Required
~# ========
~
~selected = {
~    "single": mapping.single,
~    "combined": mapping.combined,
~    "level": mapping.level,
~    "regex": mapping.regex,
~    "non_auto": mapping.non_auto,
~}


# =================================
# Needed when AI feature is enabled
# =================================

context = {
    "stu_answers": {
        "non_auto": (userargs.artifacts / 'student_solution.txt').read_text()
    },
}
```

Given that, the user prompt will be a json string:

```json
{
    "stu_answers": "Great! I put something into my answer file.\n"
}
```

Of course, more context besides the student answer can be provided:

```python
context = {
    "selected_questions": {
        "non_auto": "this is a question where it needs human inspection",
    },
    "canonicals": {
        "non_auto": "there is no canonical answer",
    },
    "stu_answers": {
        "non_auto": (userargs.artifacts / 'student_solution.txt').read_text()
    },
}
```

Then the user prompt will be:

```json
{
    "selected_questions": "this is a question where it needs human inspection",
    "canonicals": "there is no canonical answer",
    "stu_answers": "Great! I put something into my answer file.\n"
}
```

The AI feedback will be something like:

```
## non_auto

AI generated feedback:
It's great that you have started working on your answer! Just make sure to
thoroughly review the question and provide a detailed response. Keep up the good
work!
```
