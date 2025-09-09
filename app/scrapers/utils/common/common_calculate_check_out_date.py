from datetime import datetime, timedelta


def calculate_check_out_date(start_date: datetime, number_of_nights: int) -> datetime:
    """
    Calculates the check-out date based on a start date and the number of nights.

    Args:
        start_date: The starting datetime object.
        number_of_nights: The number of nights for the stay.

    Returns:
        A datetime object representing the check-out date.
    """
    if number_of_nights < 0:
        raise ValueError("number_of_nights cannot be negative.")

    return start_date + timedelta(days=number_of_nights)
