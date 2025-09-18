import json

from ...db.models import LeadHotelRunModel
from ..executors.price_executor import price_executor
from ..parsers.room_price_parser import RoomPriceParser, RoomPriceParserResponseType
from ..types.room import RoomDetails


class ServicePriceError(Exception):
    """Custom exception for service price-related errors."""

    pass


def service_price(
    params: LeadHotelRunModel, competitor_data_id: int
) -> list[RoomDetails]:
    """
    Execute price search and process the response.
    Returns CompetitorPrice if successful, None if failed.
    """
    print(f"Executing price search for competitor data ID: {competitor_data_id}")
    price_response = price_executor(params=params)

    # For debugging
    with open("price_response.json", "w") as f:
        json.dump(price_response, f, indent=4)

    if not price_response["response"]:
        raise ServicePriceError("No response data in price response")  # type: ignore

    offer_details: RoomPriceParserResponseType = RoomPriceParser(
        response=price_response["response"],
        params=params,
        competitor_data_id=competitor_data_id,
    ).parse()

    if not offer_details["successfully_parsed"]:
        raise ServicePriceError("Failed to parse price response")  # type: ignore

    offers = offer_details["offer_details"]

    with open("offers.json", "w") as f:
        json.dump(offers, f, indent=4)

    return offers
