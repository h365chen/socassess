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
```

Most of them are passed to the OpenAI python client
([openai-python](<https://github.com/openai/openai-python>)) transparently,
thereby you can refer to OpenAI's API
[here](<https://platform.openai.com/docs/api-reference/chat/create>) for
explanation on them. The only exception is the `template` key, which specifies
how socassess displays the AI feedback.

Given the above configuration, the feedback will look like:

```
AI generated feedback:
Great start! Make sure to review the question prompt carefully and ensure that
your answer file aligns with all the requirements. Keep up the good work!
```
