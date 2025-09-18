from datetime import datetime
from typing import cast

from ....db.models import LeadHotelRunModel
from .common_calculate_check_out_date import calculate_check_out_date
from .common_date_to_dict import date_to_dict


def contruct_url(params: LeadHotelRunModel) -> str:

    check_in_date = date_to_dict(
        cast(datetime, params.lead_hotel_run_request_check_in_date)
    )
    check_out_date_datetime = calculate_check_out_date(
        cast(datetime, params.lead_hotel_run_request_check_in_date),
        cast(int, params.lead_hotel_run_request_length_of_stay),
    )
    check_out_date = date_to_dict(check_out_date_datetime)
    # check_out_date = date_to_dict(params.task__parsing_end_date)
    check_in = (
        f"{check_in_date['year']}-{check_in_date['month']}-{check_in_date['day']}"
    )
    check_out = (
        f"{check_out_date['year']}-{check_out_date['month']}-{check_out_date['day']}"
    )
    adults = 2
    url = f"https://euro.expedia.net/h{params.lead_hotel_run_request_provider_id}.Hotel-Information?chkin={check_in}&chkout={check_out}&rm=a{adults}&regionId=178231&searchId=2c9757a2-5a93-45ea-8d67-29903f23e353"

    return url
