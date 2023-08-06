from ast import literal_eval


def literal_return(val):
    try:
        return literal_eval(val)
    except (ValueError, SyntaxError):
        return val
