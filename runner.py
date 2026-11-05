"""Glue code that lets the web page call the functions in target.py."""
import json
import math

import target

FUNCTIONS = [
    ("is_adult", ["age"], "True if age is 18 or more", ["20"]),
    ("celsius_to_fahrenheit", ["celsius"], "Celsius to Fahrenheit, 2 decimals", ["36.6"]),
    ("count_vowels", ["text"], "Count a, e, i, o, u (any case)", ["\"Hello World\""]),
    ("invert", ["flag"], "Opposite of a boolean", ["true"]),
    ("greet", ["name"], "Greet by name, or Guest", ["\"Mansur\""]),
    ("find_max", ["numbers"], "Largest number in a list", ["[3, 9, 2]"]),
    ("get_price", ["prices", "item"], "Price of an item in a dictionary",
     ["{\"apple\": 1.5}", "\"apple\""]),
    ("swap", ["pair"], "Swap the two values of a pair", ["[1, 2]"]),
    ("common_items", ["set_a", "set_b"], "Items found in both sets",
     ["[1, 2, 3]", "[2, 3, 4]"]),
    ("is_leap_year", ["year"], "True if the year is a leap year", ["2024"]),
    ("to_int", ["value"], "Convert a value to int", ["\"42\""]),
    ("divide", ["a", "b"], "a divided by b", ["10", "4"]),
    ("power", ["base", "exponent"], "base raised to exponent", ["2", "10"]),
    ("square_root", ["x"], "Square root of x", ["144"]),
    ("factorial", ["n"], "n factorial", ["5"]),
    ("average", ["numbers"], "Average of a list", ["[1, 2, 3, 4]"]),
]

SPECS = {name: (params, doc, example) for name, params, doc, example in FUNCTIONS}

# the web form sends JSON lists; these functions expect a set or a tuple
CONVERT = {"swap": (tuple,), "common_items": (set, set)}

MAX_FACTORIAL = 2000
MAX_EXPONENT = 10000


def describe():
    """Metadata the page uses to build one card per function."""
    return [
        {"name": name, "params": params, "doc": doc, "example": example}
        for name, params, doc, example in FUNCTIONS
    ]


def parse_value(text):
    """'12' -> 12, '[1,2]' -> list, 'null' -> None, plain words stay strings."""
    try:
        return json.loads(text)
    except ValueError:
        return text


def to_jsonable(value):
    if isinstance(value, (set, frozenset)):
        return sorted((to_jsonable(v) for v in value), key=repr)
    if isinstance(value, tuple):
        return [to_jsonable(v) for v in value]
    if isinstance(value, complex):
        return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return str(value)
    return value


def _too_large(name, args):
    if name == "factorial" and isinstance(args[0], int) and args[0] > MAX_FACTORIAL:
        return True
    if name == "power" and isinstance(args[1], (int, float)) and abs(args[1]) > MAX_EXPONENT:
        return True
    return False


def run_function(name, raw_args):
    """Run one target.py function and return a JSON-friendly dict."""
    if name not in SPECS:
        return {"ok": False, "error_type": "UnknownFunction", "message": name}
    params = SPECS[name][0]
    if len(raw_args) != len(params):
        return {"ok": False, "error_type": "BadRequest",
                "message": f"{name} needs {len(params)} value(s)"}
    try:
        args = [parse_value(str(a)) for a in raw_args]
        for i, kind in enumerate(CONVERT.get(name, ())):
            if isinstance(args[i], list):
                args[i] = kind(args[i])
        if _too_large(name, args):
            return {"ok": False, "error_type": "TooLarge",
                    "message": "input is too large for this demo site"}
        result = getattr(target, name)(*args)
    except Exception as exc:  # show every error to the user, that is the point
        message = str(exc.args[0]) if isinstance(exc, KeyError) and exc.args else str(exc)
        return {"ok": False, "error_type": type(exc).__name__, "message": message}
    return {"ok": True, "result": to_jsonable(result), "type": type(result).__name__}
