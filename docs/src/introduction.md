# Introduction

**socassess** is a command line tool to assist instructors to create
high-quality automated assessments and provide effective formative feedback. I
happened to create many automated assessments for various programming
assignments, including those involving a development board. However, creating
automated assessments that can accurately detect mistakes in students' work is
not as straightforward as many might expect.

For instance, it is challenging to predict the solutions students may produce.
As a result, the initial assessment code is likely to encounter bugs where it
gives unexpected results for unanticipated solutions. It is particularly
problematic when those solutions being marked incorrect are in fact correct
solutions. It will greatly confuse students, especially on those lacking
confidence.

Should I fix my assessment code, or should I just make an announcement about the
bug? Well, it depends. If the issue is trivial, perhaps making an announcement
and leaving it as is could suffice. However, a better approach might be:

1. **Give automated feedback only on solutions that were previously considered;**
2. **Otherwise, seek human feedback.**

While there were several other reasons such as easier assessment code management
and introducing connections among test cases, the aforementioned stratey was the
primary reason for me to create this project. I hope this tool can assist
assessment creators to develop better automated assessments.
