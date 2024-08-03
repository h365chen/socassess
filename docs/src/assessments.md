# Automated Assessments

Creating test cases is probably the simplest form of automated assessment for
students' programs. This method has been, and still is, the approach utilized by
many autograding systems, such as Gradescope.

However, there is a notable difference between using test cases for students'
programs and for regular software testing:

- **Students cannot see test case details except for the pass/fail outcome.**

The reason is simple: I would like to reuse them for future course offerings.

Given this constraint, how can I achieve the goal of providing automated
feedback only on previously considered solutions and seeking human feedback for
other cases?

Let's consider what actions software developers take when they encounter a
failed test case. Can they pinpoint the exact bug without any further analysis?
Probably not. It is often necessary for them to examine the test case details,
fix the code, and then rerun the test case. If the fix does not work, they must
repeat the process. This is often a manual process.

Apparently, we can do the same for automated assessments. If we observe any test
case failures when running a student's program, we can look into the test case
detail and the student's code, then offer the student feedback.

While this approach might seem impractical since it essentially becomes a manual
process, it actually leads us to consider an important question: *Why can't we
identify the exact bug upon seeing a failed test case?*

It is because a test case can fail for reasons that were not anticipated.

I will describe this in more detail in the next section.
