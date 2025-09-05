from .types.competitors import CompetitorData, CompetitorPrice
from .db.models import LeadHotelRunModel

def service_competitors_price(competitor_data: CompetitorData, params: LeadHotelRunModel) -> CompetitorPrice:
    # ! expedia logic
    pass
    # return CompetitorPrice(
    #     lead_hotel_hotel_id=competitor_data['lead_hotel_hotel_id']
    #     lead_hotel_provider_hotel_id=competitor_data['lead_hotel_provider_hotel_id'],
    #     lead_hotel_provider_competitor_hotel_id=competitor_data['lead_hotel_provider_competitor_hotel_id'],
    #     lead_hotel_provider_competitor_hotel_price=,
    #     lead_hotel_provider_competitor_hotel_currency=params.lead_hotel_run_request_currency,
    #     lead_hotel_provider_competitor_hotel_url=competitor_data.lead_hotel_provider_competitor_hotel_url,
    #     lead_hotel_provider_competitor_hotel_brand_offer=competitor_data.lead_hotel_provider_competitor_hotel_brand_offer,
    #     lead_hotel_provider_competitor_hotel_created_at=competitor_data.lead_hotel_provider_competitor_hotel_created_at
    # )8