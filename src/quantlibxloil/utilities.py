
def first_key(d : dict, value, default_value=None):
    """Returns the first key of a dictionary that has the specified value."""
    for k, v in d.items():
        if v == value:
            return k
    if not default_value:
        raise ValueError(f"Value {value} not found in dictionary.")
    return first_key(d, default_value, default_value=None)

UNKNOWN_KEY = "UNKNOWN"
UNKNOWN_VALUE = -1