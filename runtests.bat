copy .\testcases\inputs\add_stdin_stdout.in
copy .\testcases\outputs\add_stdin_stdout.out
copy .\testcases\programs\add_stdin_stdout.toy
python toy.py add_stdin_stdout.toy < add_stdin_stdout.in >add_stdin_stdout.output
diff add_stdin_stdout.out add_stdin_stdout.output > add_stdin_stdout.diff
del add_stdin_stdout.toy
del add_stdin_stdout.in
del add_stdin_stdout.out