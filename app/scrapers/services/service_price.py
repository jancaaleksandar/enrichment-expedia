import json
from typing import List

from ...db.models import LeadHotelRunModel
from ..executors.price_executor import price_executor
from ..parsers.room_price_parser import RoomPriceParser, RoomPriceParserResponseType
from ..types.room import RoomDetails


def service_price(
    params: LeadHotelRunModel, competitor_data_id: int
) -> List[RoomDetails]:
    """
    Execute price search and process the response.
    Returns CompetitorPrice if successful, None if failed.
    """
    price_response = price_executor(params=params)

    # For debugging
    with open("price_response.json", "w") as f:
        json.dump(price_response, f, indent=4)

    offer_details: RoomPriceParserResponseType = RoomPriceParser(
        response=price_response, params=params, competitor_data_id=competitor_data_id
    ).parse()

    if not offer_details["successfully_parsed"]:
        raise Exception("Failed to parse price response")

    offers = offer_details["offer_details"]

    with open("offers.json", "w") as f:
        json.dump(offers, f, indent=4)

    return offers
