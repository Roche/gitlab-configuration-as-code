from datetime import datetime


def validate_date(date_text, format="%Y-%m-%d"):
    try:
        datetime.strptime(date_text, format)
    except ValueError:
        return False
    return True


def is_http(text):
    return True if text.starts_with("http://") else False


def is_https(text):
    return True if text.starts_with("https://") else False
