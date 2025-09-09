from typing import List, Optional, TypedDict


class ExtraDetails(TypedDict):
    extra_details_description: str
    extra_details_price: float


class RefundableDetails(TypedDict):
    refundable_details_refundable: bool
    refundable_details_refundable_description: str


class PriceDetails(TypedDict):
    price_details_night_price: Optional[float]
    price_details_total_price: Optional[float]


class OfferDetails(TypedDict):
    offer_details_price_night: float
    offer_details_price_total: float
    offer_details_refundable: bool
    offer_details_refundable_description: str
    offer_details_extras: List[ExtraDetails] = None
    offer_details_url: str
    offer_details_competitor_data_id: Optional[int]


class RoomDetails(OfferDetails):
    room_details_name: str
    room_details_guests: int
    room_details_sold_out: bool
