from datetime import datetime

from ....db.models import LeadHotelCompetitorData, LeadHotelRunModel
from ...types.competitors import CompetitorParsedData


def map_hotel_competitor_data(
    competitor_data: list[CompetitorParsedData],
    params: LeadHotelRunModel,
) -> list[LeadHotelCompetitorData]:
    lead_hotel_competitor_data_list: list[LeadHotelCompetitorData] = []
    for competitor in competitor_data:
        lead_hotel_competitor_data = LeadHotelCompetitorData(
            lead_hotel_competitor_lead_id=params.lead_hotel_run_lead_id,
            lead_hotel_competitor_data_request_provider=params.lead_hotel_run_request_provider,
            lead_hotel_competitor_data_request_provider_id=competitor[
                "competitor_parsed_data_hotel_id"
            ],
            lead_hotel_competitor_data_request_provider_url=competitor[
                "competitor_parsed_data_hotel_url"
            ],
            lead_hotel_competitor_data_hotel_name=competitor[
                "competitor_parsed_data_hotel_name"
            ],
            lead_hotel_competitor_data_hotel_address=None,
            lead_hotel_competitor_data_hotel_coordinates=None,
            lead_hotel_competitor_data_hotel_rating_amount=None,
            lead_hotel_competitor_data_hotel_rating_type=None,
            lead_hotel_competitor_data_hotel_review_score=None,
            lead_hotel_competitor_data_hotel_review_count=None,
            lead_hotel_competitor_data_created_at=datetime.now(),
            lead_hotel_competitor_data_position=competitor[
                "competitor_parsed_data_position"
            ],
        )
        lead_hotel_competitor_data_list.append(lead_hotel_competitor_data)
    return lead_hotel_competitor_data_list
