# Automated Assessments

Creating test cases is probably the simplest form of an automated assessment on
students' programs. It has been, and still is, the approach utilized by many
autograding systems (*e.g.*, Gradescope).

However, there is a notable difference between using test cases on students'
programs and in regular software testing.

- **Students cannot see test case details except the pass/fail outcome**

The reason is simple, since I would like to re-use them for future course
offerings.

So, given this constraint, how can I achieve the target that give automated
feedback only on previously considered solutions and seek human feedback for
other cases?

Let's consider what action software developers will do when seeing a failed test
case. Can they pinpoint the exact bug without any further analysis? Probably
not, it is often needed for them to look into the test case details, fix code,
then re-run the test case. If the fix does not work, they have to repeat the
process. This is often a manual process.

Apparently, we can do the same for automated assessments. If we observe any test
case failures when running a student's program, we can look into the test case
detail and the student's code, then offer the student a feedback.

Well, that looks very stupid since it is essentially a manual process. However,
it actually leads us to think about one question: *why can't we tell the exact
bug when seeing a failed test case?*

It is because a test case can fail due to reasons that were not expected.

I will describe it in the next section.
