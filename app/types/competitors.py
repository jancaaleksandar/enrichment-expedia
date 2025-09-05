from typing import TypedDict
from datetime import datetime

class CompetitorParams(TypedDict):
    lead_hotel_run_hotel_id : int
    lead_hotel_run_provider_hotel_id : str

class CompetitorData(TypedDict):
    lead_hotel_hotel_id : str
    lead_hotel_provider_hotel_id : str
    lead_hotel_provider_competitor_hotel_id : str
    
class CompetitorPrice(CompetitorData):
    lead_hotel_provider_competitor_hotel_price : float
    lead_hotel_provider_competitor_hotel_currency : str
    lead_hotel_provider_competitor_hotel_url : str
    lead_hotel_provider_competitor_hotel_brand_offer : bool
    lead_hotel_provider_competitor_hotel_created_at : datetime