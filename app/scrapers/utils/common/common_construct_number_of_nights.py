from datetime import date


def construct_number_of_nights(check_in_date: date, check_out_date: date) -> int:
    """
    Calculates the number of nights between a check-in date and a check-out date.

    Args:
        check_in_date: The check-in date.
        check_out_date: The check-out date.

    Returns:
        The number of nights (days) between the two dates.
    """

    if check_out_date < check_in_date:
        raise ValueError("Check-out date cannot be earlier than check-in date.")

    delta = check_out_date - check_in_date
    return delta.days
