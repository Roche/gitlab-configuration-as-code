from datetime import datetime


def validate_date(date_text, format="%Y-%m-%d"):
    try:
        datetime.strptime(date_text, format)
    except ValueError:
        return False
    return True
