# Lab 6 — Code and Branch Coverage: Pet Boarding

## Tools

- Python 3.13, pytest 9.2, pytest-cov 7.1 (coverage.py)
- Command used (run inside `Lab 6/`):

```bash
python3 -m pip install pytest pytest-cov
python3 -m pytest -v --cov=pet_boarding --cov-branch --cov-report=term-missing --cov-report=html
```

## Results

| | Tests | Statements | Missed | Branches | Partial branches | Coverage |
|---|---|---|---|---|---|---|
| Before (starter tests) | 2 | 37 | 23 | 26 | 6 | **32%** |
| After (final tests) | 18 | 37 | 0 | 26 | 0 | **100%** |

Before, lines `6, 8, 11, 15-23, 28, 30, 35-45` were never executed: the error checks, the
premium bonus, all fee calculation, both early returns in `admission_ok`, and all of
`checkout_status`.

Full outputs: [`coverage_reports/coverage_before.txt`](coverage_reports/coverage_before.txt),
[`coverage_reports/coverage_after.txt`](coverage_reports/coverage_after.txt).
HTML reports: `coverage_reports/html_before/index.html`, `coverage_reports/html_after/index.html`.

## Test design

Each decision in the module was listed and a test chosen to drive it both True and False.

### `boarding_fee(pet_type, days, is_premium)`

| Decision (line) | Test | Input | Expected | Covers |
|---|---|---|---|---|
| `pet_type not in INCLUDED_DAYS` (5) | `test_unknown_pet` | `("hamster", 3, False)` | `ValueError` | True branch, line 6 |
| `days < 0` (7) | `test_negative_days` | `("cat", -1, False)` | `ValueError` | True branch, line 8 |
| `is_premium and pet_type != "rabbit"` (10) | `test_premium_cat_within_included` | `("cat", 4, True)` | `0` | True branch, line 11; `extra <= 0` True |
| | `test_premium_rabbit_no_bonus` | `("rabbit", 6, True)` | `40` | premium but rabbit → False |
| | `test_within_included_days` (given) | `("dog", 1, False)` | `0` | not premium → False; `extra <= 0` True |
| `extra <= 0` (13) | `test_cat_short_extra` | `("cat", 5, False)` | `40` | False branch |
| `pet_type == "dog"` (15) | `test_dog_short_extra` | `("dog", 5, False)` | `90` | True (rate 30) |
| | `test_cat_short_extra` | `("cat", 5, False)` | `40` | False (rate 20) |
| `extra > 10` (19) | `test_dog_long_extra` | `("dog", 15, False)` | `585` | True, nested dog True (rate 45) |
| | `test_cat_long_extra` | `("cat", 15, False)` | `360` | True, nested dog False (rate 30) |
| | `test_extra_exactly_ten` | `("cat", 13, False)` | `200` | boundary: extra = 10 → False |

### `admission_ok(pet_age_years, vaccinations, is_senior)`

| Decision (line) | Test | Input | Expected |
|---|---|---|---|
| `is_senior` True, `vaccinations >= 3` True (27–28) | `test_senior_enough_vaccines` | `(10, 3, True)` | `True` |
| `is_senior` True, `vaccinations >= 3` False | `test_senior_not_enough_vaccines` | `(10, 2, True)` | `False` |
| `pet_age_years < 1` True (29–30) | `test_too_young` | `(0.5, 5, False)` | `False` |
| `vaccinations >= 2` True (31) | `test_admission_ok` (given) | `(4, 2, False)` | `True` |
| `vaccinations >= 2` False | `test_adult_not_enough_vaccines` | `(4, 1, False)` | `False` |

### `checkout_status(minutes_left, is_long_stay, is_weekend)`

The cutoff is 30 (long stay) or 15 (short stay), plus 20 on weekends. Each result
(`open` / `late` / `closed`) is checked, and both values of each flag are used.

| Test | Flags | Cutoff | Inputs → expected |
|---|---|---|---|
| `test_long_stay_weekday` | long, weekday | 30 | 30 → open, 20 → late, 10 → closed |
| `test_short_stay_weekend` | short, weekend | 35 | 40 → open, 25 → late, 5 → closed |
| `test_short_stay_weekday` | short, weekday | 15 | 15 → open (boundary) |

## Conclusion

The two starter tests reached only 32% combined statement and branch coverage. With 16
added tests, chosen so that every `if` is taken both ways, the final suite of 18 tests
reaches 100% statement and 100% branch coverage, and all tests pass.
