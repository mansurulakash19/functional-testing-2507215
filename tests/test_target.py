"""Functional tests for every function in target.py.

For each function: valid inputs, boundary values, invalid values and wrong types.
Where the task text does not say what a wrong type should do, the test records
what the original code does today (see "Suspected bugs" in the README).
"""
import math

import pytest

import target


# ---------------------------------------------------------------- 1. is_adult
@pytest.mark.parametrize("age, expected", [
    (0, False),      # lowest allowed value
    (1, False),
    (17, False),     # just below the boundary
    (18, True),      # the boundary itself
    (19, True),      # just above the boundary
    (120, True),
    (17.9, False),   # floats around the boundary
    (18.0, True),
])
def test_is_adult_valid(age, expected):
    result = target.is_adult(age)
    assert result is expected


@pytest.mark.parametrize("age", [-1, -18, -0.5])
def test_is_adult_negative_raises_value_error(age):
    with pytest.raises(ValueError, match="age cannot be negative"):
        target.is_adult(age)


@pytest.mark.parametrize("age", ["18", "abc", None, [18]])
def test_is_adult_wrong_type_raises_type_error(age):
    with pytest.raises(TypeError):
        target.is_adult(age)


# ------------------------------------------------- 2. celsius_to_fahrenheit
@pytest.mark.parametrize("celsius, expected", [
    (0, 32.0),
    (100, 212.0),
    (-40, -40.0),          # both scales meet here
    (37, 98.6),
    (36.6, 97.88),
    (-273.15, -459.67),    # absolute zero
    (0.1, 32.18),
    (1.005, 33.81),        # rounding to 2 decimals
])
def test_celsius_to_fahrenheit_values(celsius, expected):
    assert target.celsius_to_fahrenheit(celsius) == pytest.approx(expected, abs=1e-9)


def test_celsius_to_fahrenheit_returns_float():
    assert isinstance(target.celsius_to_fahrenheit(0), float)


def test_celsius_to_fahrenheit_rounds_to_two_decimals():
    assert target.celsius_to_fahrenheit(1.23456) == 34.22


@pytest.mark.parametrize("celsius", ["20", None, [1]])
def test_celsius_to_fahrenheit_wrong_type(celsius):
    with pytest.raises(TypeError):
        target.celsius_to_fahrenheit(celsius)


# ------------------------------------------------------- 3. count_vowels
@pytest.mark.parametrize("text, expected", [
    ("", 0),
    ("bcdfg", 0),
    ("aeiou", 5),
    ("AEIOU", 5),             # ignores case
    ("Hello World", 3),
    ("y", 0),                 # y is not a vowel
    ("rhythm", 0),
    ("a e i o u", 5),
    ("12345!@#", 0),
    ("aaaa", 4),              # repeated vowels all count
    ("\u00e9\u00e8", 0),      # accented letters are not in "aeiou"
])
def test_count_vowels_valid(text, expected):
    result = target.count_vowels(text)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("value", [None, 123, 1.5, ["a"], b"abc", True])
def test_count_vowels_wrong_type(value):
    with pytest.raises(TypeError, match="text must be a string"):
        target.count_vowels(value)


# ------------------------------------------------------------ 4. invert
@pytest.mark.parametrize("flag, expected", [(True, False), (False, True)])
def test_invert_valid(flag, expected):
    result = target.invert(flag)
    assert result is expected


@pytest.mark.parametrize("flag", [0, 1, "True", "", None, [], 1.0])
def test_invert_non_bool_raises_type_error(flag):
    with pytest.raises(TypeError, match="flag must be True or False"):
        target.invert(flag)


# ------------------------------------------------------------- 5. greet
@pytest.mark.parametrize("name, expected", [
    ("Alice", "Hello, Alice!"),
    ("  Bob  ", "Hello, Bob!"),            # trimmed
    ("Mary Ann", "Hello, Mary Ann!"),      # inner space kept
    ("x", "Hello, x!"),
    (None, "Hello, Guest!"),
    ("", "Hello, Guest!"),
    ("   ", "Hello, Guest!"),
    ("\t\n", "Hello, Guest!"),
])
def test_greet_valid(name, expected):
    assert target.greet(name) == expected


def test_greet_default_argument_is_guest():
    assert target.greet() == "Hello, Guest!"


@pytest.mark.parametrize("name", [123, 1.5, ["a"], True])
def test_greet_wrong_type_raises_attribute_error(name):
    with pytest.raises(AttributeError):
        target.greet(name)


# ---------------------------------------------------------- 6. find_max
@pytest.mark.parametrize("numbers, expected", [
    ([1, 5, 3], 5),
    ([5, 1, 3], 5),
    ([3, 1, 5], 5),            # maximum at first, middle and last position
    ([-5, -1, -3], -1),
    ([7], 7),                  # single element
    ([2, 2, 2], 2),
    ([1.5, 2.5, 0.5], 2.5),
    ([1, 2.5], 2.5),           # mixed int and float
    ((4, 9, 2), 9),            # tuple is also accepted
    ([0, -1], 0),
])
def test_find_max_valid(numbers, expected):
    assert target.find_max(numbers) == expected


@pytest.mark.parametrize("numbers", [[], ()])
def test_find_max_empty_raises_value_error(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.find_max(numbers)


@pytest.mark.parametrize("numbers", [None, 5, 3.2])
def test_find_max_not_a_sequence(numbers):
    with pytest.raises(TypeError):
        target.find_max(numbers)


def test_find_max_mixed_types_cannot_be_compared():
    with pytest.raises(TypeError):
        target.find_max([1, "a"])


# --------------------------------------------------------- 7. get_price
@pytest.mark.parametrize("prices, item, expected", [
    ({"apple": 1.5, "pear": 2}, "apple", 1.5),
    ({"apple": 1.5, "pear": 2}, "pear", 2),
    ({"free": 0}, "free", 0),                 # zero price is still a price
    ({"x": None}, "x", None),                 # a stored None is returned
    ({1: "one"}, 1, "one"),                   # non-string keys
    ({"": 5}, "", 5),                         # empty-string key
])
def test_get_price_found(prices, item, expected):
    assert target.get_price(prices, item) == expected


@pytest.mark.parametrize("prices, item", [
    ({}, "apple"),
    ({"apple": 1}, "pear"),
    ({"apple": 1}, "Apple"),                  # keys are case-sensitive
    ({"apple": 1}, None),
])
def test_get_price_missing_raises_key_error(prices, item):
    with pytest.raises(KeyError, match="not found"):
        target.get_price(prices, item)


def test_get_price_error_message_names_the_item():
    with pytest.raises(KeyError, match="mango not found"):
        target.get_price({"apple": 1}, "mango")


def test_get_price_prices_is_none():
    with pytest.raises(TypeError):
        target.get_price(None, "apple")


def test_get_price_unhashable_item():
    with pytest.raises(TypeError):
        target.get_price({"apple": 1}, ["apple"])


# ------------------------------------------------------------- 8. swap
@pytest.mark.parametrize("pair, expected", [
    ((1, 2), (2, 1)),
    (("a", "b"), ("b", "a")),
    ((1, 1), (1, 1)),
    ((None, 0), (0, None)),
    ([1, 2], (2, 1)),            # a list is accepted, the result is a tuple
    ("ab", ("b", "a")),
])
def test_swap_valid(pair, expected):
    result = target.swap(pair)
    assert result == expected
    assert isinstance(result, tuple)


@pytest.mark.parametrize("pair", [(), (1,), (1, 2, 3), [], "abc"])
def test_swap_wrong_length_raises_value_error(pair):
    with pytest.raises(ValueError, match="exactly 2 values"):
        target.swap(pair)


@pytest.mark.parametrize("pair", [None, 5, 2.5])
def test_swap_not_a_sequence(pair):
    with pytest.raises(TypeError):
        target.swap(pair)


# ------------------------------------------------------ 9. common_items
@pytest.mark.parametrize("set_a, set_b, expected", [
    ({1, 2, 3}, {2, 3, 4}, {2, 3}),
    ({1, 2}, {3, 4}, set()),                 # no overlap
    (set(), {1, 2}, set()),                  # empty first set
    ({1, 2}, set(), set()),                  # empty second set
    (set(), set(), set()),
    ({1, 2}, {1, 2}, {1, 2}),                # identical
    ({1, 2, 3}, {2}, {2}),                   # subset
    ({"a", "b"}, {"b", "c"}, {"b"}),
])
def test_common_items_valid(set_a, set_b, expected):
    result = target.common_items(set_a, set_b)
    assert result == expected
    assert isinstance(result, set)


def test_common_items_does_not_change_inputs():
    a, b = {1, 2}, {2, 3}
    target.common_items(a, b)
    assert a == {1, 2}
    assert b == {2, 3}


def test_common_items_frozenset_keeps_type_of_first_argument():
    assert target.common_items(frozenset({1, 2}), {2}) == frozenset({2})


@pytest.mark.parametrize("set_a, set_b", [
    ([1, 2], [2, 3]),
    (None, {1}),
    ({1}, None),
    ("ab", "bc"),
])
def test_common_items_wrong_type(set_a, set_b):
    with pytest.raises(TypeError):
        target.common_items(set_a, set_b)


# ---------------------------------------------------- 10. is_leap_year
@pytest.mark.parametrize("year, expected", [
    (1, False),       # smallest allowed year
    (4, True),
    (100, False),     # divisible by 100 but not 400
    (200, False),
    (400, True),      # divisible by 400
    (1900, False),
    (2000, True),
    (2023, False),
    (2024, True),
    (2100, False),
    (2400, True),
    (1999, False),
    (2001, False),
])
def test_is_leap_year_valid(year, expected):
    result = target.is_leap_year(year)
    assert result is expected


@pytest.mark.parametrize("year", [0, -1, -400, 0.5])
def test_is_leap_year_below_one_raises_value_error(year):
    with pytest.raises(ValueError, match="year must be 1 or more"):
        target.is_leap_year(year)


@pytest.mark.parametrize("year", [None, "2000", [2000]])
def test_is_leap_year_wrong_type(year):
    with pytest.raises(TypeError):
        target.is_leap_year(year)


# ---------------------------------------------------------- 11. to_int
@pytest.mark.parametrize("value, expected", [
    ("42", 42),
    ("-7", -7),
    (" 12 ", 12),         # surrounding spaces are allowed by int()
    ("0", 0),
    (5, 5),
    (0, 0),
    (3.9, 3),             # float is truncated, not rounded
    (-3.9, -3),
    (3.0, 3),
])
def test_to_int_valid(value, expected):
    result = target.to_int(value)
    assert result == expected
    assert type(result) is int


@pytest.mark.parametrize("value", [True, False])
def test_to_int_bool_raises_type_error(value):
    with pytest.raises(TypeError, match="bool is not allowed"):
        target.to_int(value)


@pytest.mark.parametrize("value", ["abc", "", "3.5", "1,000", float("nan")])
def test_to_int_invalid_value_raises_value_error(value):
    with pytest.raises(ValueError):
        target.to_int(value)


def test_to_int_infinity_raises_overflow_error():
    with pytest.raises(OverflowError):
        target.to_int(float("inf"))


@pytest.mark.parametrize("value", [None, [1], {"a": 1}, (1, 2)])
def test_to_int_wrong_type(value):
    with pytest.raises(TypeError):
        target.to_int(value)


# ----------------------------------------------------------- 12. divide
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5.0),
    (7, 2, 3.5),
    (-6, 3, -2.0),
    (6, -3, -2.0),
    (-6, -3, 2.0),
    (0, 5, 0.0),
    (5, 1, 5.0),
    (1.5, 0.5, 3.0),
])
def test_divide_valid(a, b, expected):
    result = target.divide(a, b)
    assert result == expected
    assert isinstance(result, float)


def test_divide_inexact_result():
    assert target.divide(1, 3) == pytest.approx(0.3333333333)


@pytest.mark.parametrize("a, b", [(5, 0), (5, 0.0), (0, 0), (-5, 0), (1.5, -0.0)])
def test_divide_by_zero(a, b):
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        target.divide(a, b)


@pytest.mark.parametrize("a, b", [("a", 1), (1, "a"), (None, 1), (1, None), ([1], 2)])
def test_divide_wrong_type(a, b):
    with pytest.raises(TypeError):
        target.divide(a, b)


# ----------------------------------------------------------- 13. power
@pytest.mark.parametrize("base, exponent, expected", [
    (2, 3, 8),
    (2, 0, 1),
    (0, 0, 1),            # Python defines 0 ** 0 as 1
    (0, 5, 0),
    (5, 1, 5),
    (-2, 3, -8),
    (-2, 2, 4),
    (1, 1000, 1),
    (2, 10, 1024),
    (2, 100, 1267650600228229401496703205376),   # very large integer
])
def test_power_integer_results(base, exponent, expected):
    result = target.power(base, exponent)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("base, exponent, expected", [
    (2, -1, 0.5),
    (4, 0.5, 2.0),
    (2.5, 2, 6.25),
    (10, -2, 0.01),
])
def test_power_float_results(base, exponent, expected):
    assert target.power(base, exponent) == pytest.approx(expected)


def test_power_negative_base_fractional_exponent_is_complex():
    assert isinstance(target.power(-8, 0.5), complex)


def test_power_zero_to_negative_exponent():
    with pytest.raises(ZeroDivisionError):
        target.power(0, -1)


@pytest.mark.parametrize("base, exponent", [("a", 2), (2, "a"), (None, 2), (2, None)])
def test_power_wrong_type(base, exponent):
    with pytest.raises(TypeError):
        target.power(base, exponent)


# ------------------------------------------------------ 14. square_root
@pytest.mark.parametrize("x, expected", [
    (0, 0.0),
    (1, 1.0),
    (4, 2.0),
    (0.25, 0.5),
    (144, 12.0),
    (1e10, 100000.0),
])
def test_square_root_exact(x, expected):
    result = target.square_root(x)
    assert result == expected
    assert isinstance(result, float)


def test_square_root_inexact():
    assert target.square_root(2) == pytest.approx(1.41421356237)


@pytest.mark.parametrize("x", [-1, -0.0001, -100])
def test_square_root_negative_raises_value_error(x):
    with pytest.raises(ValueError, match="cannot take the square root"):
        target.square_root(x)


def test_square_root_infinity_and_nan():
    assert target.square_root(float("inf")) == float("inf")
    assert math.isnan(target.square_root(float("nan")))


@pytest.mark.parametrize("x", ["4", None, [4]])
def test_square_root_wrong_type(x):
    with pytest.raises(TypeError):
        target.square_root(x)


# --------------------------------------------------------- 15. factorial
@pytest.mark.parametrize("n, expected", [
    (0, 1),                      # 0! is 1
    (1, 1),
    (2, 2),
    (5, 120),
    (10, 3628800),
    (20, 2432902008176640000),
    (25, 15511210043330985984000000),
])
def test_factorial_valid(n, expected):
    result = target.factorial(n)
    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("n", [-1, -5, -100])
def test_factorial_negative_raises_value_error(n):
    with pytest.raises(ValueError, match="not defined for negative numbers"):
        target.factorial(n)


@pytest.mark.parametrize("n", [2.5, 3.0, "5", None, [3]])
def test_factorial_wrong_type_raises_type_error(n):
    with pytest.raises(TypeError):
        target.factorial(n)


# ---------------------------------------------------------- 16. average
@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 2.0),
    ([5], 5.0),                  # single element
    ([1, 2], 1.5),
    ([-1, 1], 0.0),
    ([-4, -2], -3.0),
    ([0, 0, 0], 0.0),
    ((2, 4, 6), 4.0),            # tuple input
    ([1.5, 2.5], 2.0),
])
def test_average_valid(numbers, expected):
    result = target.average(numbers)
    assert result == expected
    assert isinstance(result, float)


def test_average_inexact_result():
    assert target.average([0.1, 0.2, 0.3]) == pytest.approx(0.2)


@pytest.mark.parametrize("numbers", [[], ()])
def test_average_empty_raises_value_error(numbers):
    with pytest.raises(ValueError, match="list is empty"):
        target.average(numbers)


@pytest.mark.parametrize("numbers", [None, 5])
def test_average_not_a_sequence(numbers):
    with pytest.raises(TypeError):
        target.average(numbers)


def test_average_non_numeric_items():
    with pytest.raises(TypeError):
        target.average(["a", "b"])
def test_demo_red():
    assert target.is_adult(17) is True
    