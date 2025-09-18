from typing import TypedDict


class ExtraDetails(TypedDict):
    extra_details_description: str
    extra_details_price: float


class RefundableDetails(TypedDict):
    refundable_details_refundable: bool
    refundable_details_refundable_description: str


class PriceDetails(TypedDict):
    price_details_night_price: float | None
    price_details_total_price: float | None


class OfferDetails(TypedDict):
    offer_details_price_night: float
    offer_details_price_total: float
    offer_details_refundable: bool
    offer_details_refundable_description: str
    offer_details_extras: list[ExtraDetails] | None
    offer_details_url: str
    offer_details_competitor_data_id: int | None


class RoomDetails(OfferDetails):
    room_details_name: str
    room_details_guests: int
    room_details_sold_out: bool
