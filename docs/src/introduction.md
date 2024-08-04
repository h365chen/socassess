# Introduction

**socassess** is a command line tool designed to help instructors create
high-quality automated assessments and provide effective formative feedback. I
have created many automated assessments for various programming assignments,
including those that involve a development board. However, creating automated
assessments that can accurately detect mistakes in students' work is not as
straightforward as one might expect.

For instance, it can be challenging to predict the solutions students may
produce. As a result, the initial assessment code is likely to encounter bugs,
leading to unexpected results for unanticipated solutions. This is particularly
problematic when correct solutions are mistakenly marked as incorrect, which can
greatly confuse students, especially those lacking confidence.

Should I fix my assessment code, or should I just make an announcement about the
bug? Well, it depends. If the issue is trivial, perhaps making an announcement
and leaving it as is could suffice. However, a better *approach* might be:

1. **Give automated feedback only on solutions that were previously
   considered;**
1. **Otherwise, seek human feedback.**

There were several other reasons for creating this project, such as easier
assessment code management and introducing connections among test cases.
However, the primary reason was to achieve the aforementioned approach. I hope
this tool can assist assessment creators in developing better automated
assessments.
