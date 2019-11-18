def is_blank(string):
    # type: (str)-> bool
    return not (string and string.strip())


def is_not_blank(string):
    # type: (str)-> bool
    return bool(string and string.strip())
