import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status

# Example test cases:
def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0

def test_admission_ok():
    assert admission_ok(4, 2, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.

def test_unknown_pet():
    with pytest.raises(ValueError):
        boarding_fee("hamster", 3, False)

def test_negative_days():
    with pytest.raises(ValueError):
        boarding_fee("cat", -1, False)

def test_premium_cat_within_included():
    assert boarding_fee("cat", 4, True) == 0

def test_premium_rabbit_no_bonus():
    assert boarding_fee("rabbit", 6, True) == 40

def test_dog_short_extra():
    assert boarding_fee("dog", 5, False) == 90

def test_cat_short_extra():
    assert boarding_fee("cat", 5, False) == 40

def test_dog_long_extra():
    assert boarding_fee("dog", 15, False) == 585

def test_cat_long_extra():
    assert boarding_fee("cat", 15, False) == 360

def test_extra_exactly_ten():
    assert boarding_fee("cat", 13, False) == 200

def test_senior_enough_vaccines():
    assert admission_ok(10, 3, True) is True

def test_senior_not_enough_vaccines():
    assert admission_ok(10, 2, True) is False

def test_too_young():
    assert admission_ok(0.5, 5, False) is False

def test_adult_not_enough_vaccines():
    assert admission_ok(4, 1, False) is False

def test_long_stay_weekday():
    assert checkout_status(30, True, False) == "open"
    assert checkout_status(20, True, False) == "late"
    assert checkout_status(10, True, False) == "closed"

def test_short_stay_weekend():
    assert checkout_status(40, False, True) == "open"
    assert checkout_status(25, False, True) == "late"
    assert checkout_status(5, False, True) == "closed"

def test_short_stay_weekday():
    assert checkout_status(15, False, False) == "open"
