# INSTRUCTOR ONLY — do not distribute

## Breaker mutants: which tests catch which bugs?

`check_tests.py` plants 8 realistic bugs in the known-good importer, one at a time, and runs the test modules you name against each one. It uses only the standard library, works offline, and takes about a second.

```bash
# from the pack root
python3 instructor/tools/breaker-mutants/check_tests.py sandbox/panic-pantry tests.test_importer_contract
python3 instructor/tools/breaker-mutants/check_tests.py sandbox/worktrees/orchestrated \
    tests.test_importer_contract tests.test_promo_import
```

**What it backs:** Module 1 says the frozen contract tests catch only 4 of 8 planted bugs. Run the first command to show it:

| Bug | What it does | Contract tests |
|---|---|---|
| `local_threshold` | Decides pending vs. active itself, with `>= 20` | caught |
| `dup_as_error` | Reports duplicates as errors | caught |
| `auto_approve` | Approves every pending code, so `FREE-ALL` goes live | caught |
| `line_off_by_one` | Numbers the first data row 1 | caught |
| `blank_reason` | Says "blank line" instead of "empty row" | **missed** |
| `bad_header_still_imports` | Flags a wrong header, then imports every row anyway | **missed** |
| `extra_columns_ok` | Accepts rows with 3+ columns | **missed** |
| `fraction_rounds_down` | Accepts `20.9` as `20` | **missed** |

**Other uses:**

- **Grade a Breaker (Ex4, capstone).** Run it on the learner's worktree with `tests.test_promo_import` added. A strong Breaker card produces tests that catch most of the four the contract misses.
- **Level up L5.2 ("test the tester").** Learners plant one of these bugs themselves and see whether their tests notice.

**Notes:**

- The script generates its mutants from `instructor/solutions/importer_solution.py`. If you change the solution, the script stops and names any mutant that no longer applies. It never edits the solution.
- It restores the checkout's own `importer.py` (or its absence) when it finishes.
- `correct` must pass every module you pass in. "FAILS on correct code!" means a test is wrong, not the importer.
