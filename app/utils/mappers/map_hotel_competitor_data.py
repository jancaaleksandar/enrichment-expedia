from typing import List
from app.types.competitors import CompetitorData
from app.db.models import LeadHotelCompetitorData


def map_hotel_competitor_data(competitor_data : List[CompetitorData]) -> List[LeadHotelCompetitorData]:
    lead_hotel_competitor_data_list: List[LeadHotelCompetitorData] = []
    for competitor in competitor_data:
        lead_hotel_competitor_data = LeadHotelCompetitorData(
            lead_hotel_competitor_data_request_provider=competitor.lead_hotel_competitor_data_request_provider,
            lead_hotel_competitor_data_request_provider_id=competitor.lead_hotel_competitor_data_request_provider_id,
            lead_hotel_competitor_data_request_provider_url=competitor.lead_hotel_competitor_data_request_provider_url,
            lead_hotel_competitor_data_hotel_name=competitor.lead_hotel_competitor_data_hotel_name,
            lead_hotel_competitor_data_hotel_address=competitor.lead_hotel_competitor_data_hotel_address,
            lead_hotel_competitor_data_hotel_coordinates=competitor.lead_hotel_competitor_data_hotel_coordinates,
            lead_hotel_competitor_data_hotel_rating_amount=competitor.lead_hotel_competitor_data_hotel_rating_amount,
            lead_hotel_competitor_data_hotel_rating_type=competitor.lead_hotel_competitor_data_hotel_rating_type,
            lead_hotel_competitor_data_hotel_review_score=competitor.lead_hotel_competitor_data_hotel_review_score,
            lead_hotel_competitor_data_hotel_review_count=competitor.lead_hotel_competitor_data_hotel_review_count,
            lead_hotel_competitor_data_created_at=competitor.lead_hotel_competitor_data_created_at
        )
        lead_hotel_competitor_data_list.append(lead_hotel_competitor_data)
    return lead_hotel_competitor_data_list