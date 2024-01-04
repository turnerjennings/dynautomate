def is_float(s):
    try:
        float_value = float(s)
        return True
    except ValueError:
        return False