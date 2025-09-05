from typing import TypedDict

class RequestIngestionReceivedParam(TypedDict):
    param_date_check_in_date : str
    param_date_length_of_stay : int
    param_hotel_google_id : str
    param_region : str
    param_run_id : int
    param_lead_id : int