# Missing Dependencies

Unexpected failure is about potential issues within each test case. However, a
test case could also fail because its a prerequisite test case has failed.

In general, when it comes to unit testing, most people will think that test
cases should be isolated from others. It does work. It is because software
developers are aware of the test case details, and can recognize connected test
cases. This setting, however, does not work in automated assessments, given the
constraint that students cannot see test case details.

| name               | outcome |
|--------------------|---------|
| `check_property_A` | passed  |
| `check_property_B` | failed  |
| `check_property_C` | failed  |

For example, in the above scenario, it can happen that property *C* depends on
property *B* to satisfy. Therefore, if `check_propperty_B` fails,
`check_property_C` is bound to fail. However, students are unaware of those
implicit dependencies since they have no knowledge of their details.
Consequently, they might mistakenly believe there are issues with properties
other than property *B*, even though resolving the issue with property *B* would
lead to all test cases to pass.

It is better to have students see the following, where `check_property_C` is
explicitly marked as `skipped`.

| name               | outcome |
|--------------------|---------|
| `check_property_A` | passed  |
| `check_property_B` | failed  |
| `check_property_C` | skipped |

## Solution

If we really think about the problem, it is not truly an implementation problem.
Instead, it is a problem that assessment creators often fail to acknowledge its
existence. The reason is that many assessment creators of automated assessments
use the unit testing philosophy, where test cases should be considered isolated.
This issue can be addressed if assessment creators recognize and consider
dependencies among test cases when composing them.

The actual implementation is flexible. One approach is that every test case
generates a file which includes its outcome. If a test case has prerequisite
test cases, then it can check if corresponding files all have the test outcome
as `passed`. There are certainly many other approaches, but I will demonstrate
how I implement it using the `pytest` framework with the `pytest-dependency`
plugin.
