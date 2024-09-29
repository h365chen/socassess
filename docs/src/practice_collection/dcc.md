# `dcc`

Link to its repo: <https://github.com/COMP1511UNSW/dcc>

As its README says:

> `dcc` is a tool helps novice C programmers by catching common errors and
> providing easy-to-understand explanations.
>
> For example:
>
> dcc add extra runtime checking for errors and prints information likely to be
> helpful to novice programmers, including printing values of variables and
> expressions. Run-time checking includes array indices, for example:
>
> ```
> $ gcc count_zero.c
> $ ./a.out
> 9
>
> $ dcc count_zero.c
> $ ./a.out
> count_zero.c.c:7:7: runtime error - index 10 out of bounds for type 'int [10]'
> dcc explanation: You are using an illegal array index: 10
>   Valid indices for an array of size 10 are 0..9
>   Make sure the size of your array is correct.
>   Make sure your array indices are correct.
> Execution stopped in main() in count_zero.c at line 7:
>
> int main(void) {
> 	int numbers[10] = {0};
> 	int count = 0;
> 	for (int i = 1; i <= 10; i++) {
> -->		if (numbers[i] > 0) {
> 			count++;
> 		}
> 	}
>
> Values when execution stopped:
> count = 0
> i = 10
> numbers = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
> numbers[i] = <uninitialized value>
> ```

To build it, simply do `make dcc`. It will put together necessary files into a
folder `_build` (the default folder assigned to `BUILD_DIR`) and then remove it.
The final executable `dcc` is just a zip over the `_build` folder. As indicated
by the last few log lines of `make dcc`.

```bash
~rm -rf _build
~mkdir -p _build/embedded_src
~touch _build/embedded_src/__init__.py
~echo 'VERSION = "'`git describe --tags`'"' >_build/version.py
~for f in run_time_python/colors.py run_time_python/drive_gdb.py run_time_python/explain_context.py run_time_python/explain_error.py run_time_python/explain_output_difference.py run_time_python/gdb_interface.py run_time_python/start_gdb.py run_time_python/util.py run_time_python/watch_valgrind.py wrapper_c/dcc_check_output.c wrapper_c/dcc_dual_sanitizers.c wrapper_c/dcc_main.c wrapper_c/dcc_save_stdin.c wrapper_c/dcc_util.c wrapper_c/dcc_io.cpp; do ln -sf ../../$f _build/embedded_src; done
~for f in compile_time_python/__main__.py compile_time_python/colors.py compile_time_python/compile.py compile_time_python/compiler_explanations.py compile_time_python/explain_compiler_output.py compile_time_python/options.py compile_time_python/util.py; do ln -sf ../$f _build; done
~# --symlinks here breaks pkgutil.read_data in compile.py
~cd _build; zip dcc.zip -9 -r *.py embedded_src
~  adding: __main__.py (deflated 6%)
~  adding: colors.py (deflated 50%)
~  adding: compile.py (deflated 72%)
~  adding: compiler_explanations.py (deflated 78%)
~  adding: explain_compiler_output.py (deflated 73%)
~  adding: options.py (deflated 72%)
~  adding: util.py (deflated 65%)
~  adding: version.py (stored 0%)
~  adding: embedded_src/ (stored 0%)
~  adding: embedded_src/explain_error.py (deflated 72%)
~  adding: embedded_src/util.py (deflated 65%)
~  adding: embedded_src/explain_context.py (deflated 72%)
~  adding: embedded_src/__init__.py (stored 0%)
~  adding: embedded_src/dcc_main.c (deflated 72%)
~  adding: embedded_src/dcc_io.cpp (deflated 64%)
~  adding: embedded_src/dcc_save_stdin.c (deflated 60%)
~  adding: embedded_src/watch_valgrind.py (deflated 66%)
~  adding: embedded_src/dcc_check_output.c (deflated 75%)
~  adding: embedded_src/dcc_util.c (deflated 72%)
~  adding: embedded_src/explain_output_difference.py (deflated 74%)
~  adding: embedded_src/start_gdb.py (deflated 65%)
~  adding: embedded_src/dcc_dual_sanitizers.c (deflated 79%)
~  adding: embedded_src/gdb_interface.py (deflated 64%)
~  adding: embedded_src/drive_gdb.py (deflated 57%)
~  adding: embedded_src/colors.py (deflated 50%)
echo '#!/usr/bin/env python3' >dcc
cat _build/dcc.zip >>dcc
chmod 755 dcc
~rm -rf _build
```

To inspect the codebase, I changed the line in the Makefile, so that I can
inspect the files being zipped.

```diff
~dcc: $(SOURCE) $(EMBEDDED_SOURCE) Makefile
~    rm -rf $(BUILD_DIR)
~    mkdir -p $(PACKAGE_DIR)
~    touch $(PACKAGE_DIR)/__init__.py
~    echo 'VERSION = "'`git describe --tags`'"' >$(BUILD_DIR)/version.py
~    for f in $(EMBEDDED_SOURCE); do ln -sf ../../$$f $(PACKAGE_DIR); done
~    for f in $(SOURCE); do ln -sf ../$$f $(BUILD_DIR); done
~    # --symlinks here breaks pkgutil.read_data in compile.py
~    cd $(BUILD_DIR); zip $@.zip -9 -r *.py $(EMBEDDED_PACKAGE_NAME)
    echo '#!/usr/bin/env python3' >$@
    cat $(BUILD_DIR)/$@.zip >>$@
    chmod 755 $@
-   rm -rf $(BUILD_DIR)
+   # rm -rf $(BUILD_DIR)
```
