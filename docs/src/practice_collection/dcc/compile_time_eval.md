# Compile time evaluation

The entry file is `compile.py`. There are four essential steps.

- Update configurations in the wrapper source code (`update_wrapper_source`)
- Compile the wrapper code into an object file (`compile_wrapper_source`, called
  by `execute_compiler`)
- Compile student's code using the object file (`execute_compiler`), with
  sanitize flags configured (`-fsanitize=memory`, `-fsanitize=address`, etc.)
- Show explanations if there is a compile error message
  (`explain_compiler_output`)

The added complexity stem from compiling the wrapper source code, but other than
that, it is just a normal compilation procedure, plus a step which captures the
compile messages and map them into novice-friendly messages. Relevant code for
mapping messages are put inside `explain_compiler_output.py` and
`compiler_explanations.py`.

We will talk more about the wrapper code when discussing how `dcc` provides
novice-friendly explanations for runtime errors.
