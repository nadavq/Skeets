def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    raise ValueError(f"Cannot convert {value!r} to bool")
