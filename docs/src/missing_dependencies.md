# Missing Dependencies

Unexpected failure is about potential issues within each test case. However, a
test case could also fail because its prerequisite test case has failed.

Generally, when it comes to unit testing, most people will think that test cases
should be isolated from others. This approach works because software developers
are aware of the test case details and can recognize connected test cases.
However, this setting does not work in automated assessments, given the
constraint that students cannot see test case details.

| name | outcome |
|--------------------|---------|
| `check_property_A` | passed |
| `check_property_B` | failed |
| `check_property_C` | failed |

For example, in the scenario above, it can happen that property _C_ depends on
property _B_ being satisfied. Therefore, if `check_property_B` fails,
`check_property_C` is bound to fail. However, students are unaware of these
implicit dependencies since they have no knowledge of their details.
Consequently, they might mistakenly believe there are issues with properties
other than property _B_, even though resolving the issue with property _B_ could
lead all test cases to pass.

It would be better for students to see the following, where `check_property_C`
is explicitly marked as `skipped`.

| name | outcome |
|--------------------|---------|
| `check_property_A` | passed |
| `check_property_B` | failed |
| `check_property_C` | skipped |

## Solution

If we truly consider the problem, it is not just an implementation issue.
Instead, it is a problem that assessment creators often fail to acknowledge. The
reason is that many assessment creators of automated assessments adopt the unit
testing philosophy, where test cases should be considered isolated. This issue
can be addressed if assessment creators recognize and consider dependencies
among test cases when composing them.

The actual implementation is flexible. One approach is that every test case
generates a file which includes its outcome. If a test case has prerequisite
test cases, then it can check if corresponding files all have the test outcome
as `passed`. There are certainly many other approaches, but I will demonstrate
how I implement it using the `pytest` framework with the `pytest-dependency`
plugin.
