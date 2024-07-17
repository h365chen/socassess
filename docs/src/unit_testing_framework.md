# Unit Testing Framework

A weird mis-understanding of automated assessments is that people think it is
trivial to create them. However, my experience tells me that it is in fact a
difficult task.

The first time when I created an automated assessment to grade students'
programs, I wrote almost everything from sratch, because I thought it might just
be few lines of code to compare the output from the student's program and the
expected output. However, soon I realized that what I needed to write was not
just the lines to compare the outputs. Additionally, I had to write bunch of
code to properly iterate students' programs, clean up any intermediate results,
and collect grades and feedback. All those things had distracted me a lot.

Further, I also realized that the assessment code should be organized flexibly.
For instance, if an assignment contained two questions in a previous course
offering, and you created assessment code to assess both questions, but later
you decided to split the assignment into two smaller assignments with each
contains only one question. In that case, you want your assessment code to be
conveniently re-constructed.
