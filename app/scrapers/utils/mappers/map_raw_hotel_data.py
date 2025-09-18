from collections.abc import Sequence
from datetime import datetime

from ....db.models import LeadHotelRunModel, RawHotelData
from ...types.room import RoomDetails


def map_raw_hotel_data(
    room_offer_details: Sequence[RoomDetails],
    params: LeadHotelRunModel,
) -> list[RawHotelData]:
    raw_hotel_data_list: list[RawHotelData] = []
    for detail in room_offer_details:
        raw_hotel_data = RawHotelData(
            raw_hotel_data_lead_id=params.lead_hotel_run_lead_id,
            raw_hotel_data_run_id=params.lead_hotel_run_id,
            raw_hotel_data_request_provider=params.lead_hotel_run_request_provider,
            raw_hotel_data_request_provider_id=params.lead_hotel_run_request_provider_id,
            raw_hotel_data_request_provider_url=detail["offer_details_url"],
            raw_hotel_data_request_region=params.lead_hotel_run_request_region,
            raw_hotel_data_price_check_in_date=params.lead_hotel_run_request_check_in_date,
            raw_hotel_data_price_sold_out=detail["room_details_sold_out"],
            raw_hotel_data_price_amount=detail["offer_details_price_night"],
            raw_hotel_data_price_currency="EUR",
            raw_hotel_data_price_provider=params.lead_hotel_run_request_provider,
            raw_hotel_data_price_provider_url=detail["offer_details_url"],
            raw_hotel_data_price_provider_icon_url=None,
            raw_hotel_data_price_brand_offer=False,
            raw_hotel_data_competitor_data_id=detail[
                "offer_details_competitor_data_id"
            ],
            raw_hotel_data_room_name=detail["room_details_name"],
            raw_hotel_data_run_type=params.lead_hotel_run_type,
            raw_hotel_data_created_at=datetime.now(),
        )
        raw_hotel_data_list.append(raw_hotel_data)
    return raw_hotel_data_list
