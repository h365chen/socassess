# Seek Human Feedback through Email

In order to send an email when automated feedback is not available, we have to
configure several keys in the `socassess.toml`. The most essential keys are
listed here:

```toml
[feature]
email = true

~[email]
~
[email.account]
account = 'account'  # the sender account of the mail server
password = "pswd"  # the password to login to the mail server
from = 'from@address.com'  # the email address to use under the account
to = "to@address.com"  # to which address the email is sent, i.e., the expert email
smtp_server = "smtp.server.com"  # the SMTP server to use
```

Like normal email service, you need an _account_ and _password_ for login to
access its service. An account can manage multiple _from_ addresses. When
sending an email, a specific from address needs to be specified. The email will
then be sent using the _Simple Mail Transfer Protocol_ (SMTP)---it is a protocol
used to send emails across email servers while sender and recipient can be on
different email services.

The content of the email can be customized.

```toml
[email.content]
subject = "[socassess][Assignment 1] Human feedback needed"
email_body = '''
socassess is needing human feedback.
The attached files contain relevant context of the submission.

See attachments
'''
initial_reply = '''
An instructor has been notified for questions where pre-coded feedback are not available.
'''  # the initial feedback to be shown while waiting for human feedback
```

To make it more easier to inspect, we can attach files in the email. By default,
socassess will only attach a `draft_feedback.txt` file. It is useful when the AI
feature is enabled (`ai = true`), since it allows instructors to review the
generated AI feedback.

This is what student will see with several lines hidden:

```feedback
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

AI generated feedback:
Great start! Make sure to review the question prompt carefully and ensure that
your answer file aligns with all the requirements. Keep up the good work!

## _email

An instructor has been notified for questions where pre-coded feedback are not available.
```

This is the email:

![email_default_attachment_with_ai_enabled](figs/email_default_attachment_with_ai_enabled.png
"By default, the email only has the draft_feedback.txt as the attachment")

To add more attachments, socassess requires those files to be put inside an
**_attachment.txt** file, and all files---including the \_attachment.txt---have
to be inside the artifacts folder. Any additional attachment will be renamed
with a `.txt` suffix.

For example, in
[`a1`](<https://github.com/h365chen/socassess/blob/main/examples/a1/a1/>),
`test_email` created the \_attachment.txt and added a line
`student_solution.txt` into it. Therefore, the email contains two attachments:
*draft_feedback.txt* and *student_solution.txt.txt*

```python
def test_email(artifacts, stu_answer):
    """Prepare email attachments.

    socassess uses _attachments.txt to determine what to attach in the email.
    Here it sends out the student solution file.

    """
    with (artifacts / '_attachments.txt').open('a') as f:
        f.write(stu_answer.name)
    assert 0, "failed due to unknown reason"
```

```
artifacts/
    report.xml

    _attachments.txt
        # content of _attachments.txt
        student_solution.txt

    student_solution.txt
        # content of student_solution.txt
        Great! I put something into my answer file.
```

![email_multiple_attachment_with_ai_enabled](figs/email_multiple_attachment_with_ai_enabled.png
"Attached multiple attachments to the email")
