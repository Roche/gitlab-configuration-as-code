def is_blank(string):
    return not (string and string.strip())


def is_not_blank(string):
    return bool(string and string.strip())
