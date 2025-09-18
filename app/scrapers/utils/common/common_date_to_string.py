from datetime import datetime


def date_to_string_from_dict(date_dict: dict[str, int]) -> str:
    return f"{date_dict['year']}-{date_dict['month']}-{date_dict['day']}"


def date_to_string_from_datetime(date: datetime) -> str:
    return f"{date.year}-{date.month}-{date.day}"
