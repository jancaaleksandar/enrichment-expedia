from datetime import datetime


def date_to_dict(date: datetime) -> dict[str, int]:
    return {"year": date.year, "month": date.month, "day": date.day}
