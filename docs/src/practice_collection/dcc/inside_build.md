# Inside `_build`

The folder structure looks like:

```bash
dcc/_build
├── dcc.zip                             # <-- final executable
├── __main__.py                         # dcc/compile_time_python/__main__.py
├── colors.py                           # dcc/compile_time_python/colors.py
├── compile.py                          # dcc/compile_time_python/compile.py
├── compiler_explanations.py            # dcc/compile_time_python/compiler_explanations.py
├── explain_compiler_output.py          # dcc/compile_time_python/explain_compiler_output.py
├── options.py                          # dcc/compile_time_python/options.py
├── util.py                             # dcc/compile_time_python/util.py
├── embedded_src
│   ├── __init__.py
│   ├── dcc_check_output.c              # dcc/wrapper_c/dcc_check_output.c
│   ├── dcc_dual_sanitizers.c           # dcc/wrapper_c/dcc_dual_sanitizers.c
│   ├── dcc_io.cpp                      # dcc/wrapper_c/dcc_io.cpp
│   ├── dcc_main.c                      # dcc/wrapper_c/dcc_main.c
│   ├── dcc_save_stdin.c                # dcc/wrapper_c/dcc_save_stdin.c
│   ├── dcc_util.c                      # dcc/wrapper_c/dcc_util.c
│   ├── colors.py                       # dcc/run_time_python/colors.py
│   ├── drive_gdb.py                    # dcc/run_time_python/drive_gdb.py
│   ├── explain_context.py              # dcc/run_time_python/explain_context.py
│   ├── explain_error.py                # dcc/run_time_python/explain_error.py
│   ├── explain_output_difference.py    # dcc/run_time_python/explain_output_difference.py
│   ├── gdb_interface.py                # dcc/run_time_python/gdb_interface.py
│   ├── start_gdb.py                    # dcc/run_time_python/start_gdb.py
│   ├── util.py                         # dcc/run_time_python/util.py
│   └── watch_valgrind.py               # dcc/run_time_python/watch_valgrind.py
└── version.py
```

We can clearly see that `dcc` has two parts in checking student's code:

- compile time evaluation
- runtime evaluation

In order to conduct runtime evaluation, C code put inside the folder
`wrapper_c/` are needed. Student's code is instrumented by these C code so that
runtime context can be captured; otherwise, student's program might simply
produce a `segment fault` message providing no useful information.
