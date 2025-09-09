from datetime import datetime
from typing import TypedDict


class CompetitorParams(TypedDict):
    lead_hotel_run_hotel_id: int
    lead_hotel_run_provider_hotel_id: str


class CompetitorParsedData(TypedDict):
    competitor_parsed_data_hotel_id: str
    competitor_parsed_data_hotel_name: str
    competitor_parsed_data_hotel_url: str


class CompetitorPrice(CompetitorParsedData):
    lead_hotel_provider_competitor_hotel_price: float
    lead_hotel_provider_competitor_hotel_currency: str
    lead_hotel_provider_competitor_hotel_url: str
    lead_hotel_provider_competitor_hotel_brand_offer: bool
    lead_hotel_provider_competitor_hotel_created_at: datetime
