import json

from sqlalchemy.orm import Session

from ...db.db_functions import DatabaseFunctions
from ...db.models import LeadHotelCompetitorData, LeadHotelRunModel
from ..executors.competitor_search_executor import competitor_search_executor
from ..parsers.competitor_details_parser import (
    CompetitorDetailsParser,
    CompetitorDetailsParserResponse,
)
from ..utils.mappers.map_hotel_competitor_data import map_hotel_competitor_data


class ServiceCompetitorSearchError(Exception):
    """Custom exception for service competitor search-related errors."""

    pass


def service_competitors_search(
    request_params: LeadHotelRunModel, database_session: Session
) -> list[LeadHotelCompetitorData]:
    # Fetch any existing competitor data for this lead and provider
    existing_competitor_data = DatabaseFunctions.get_hotel_competitor_data(
        database_session=database_session, request_params=request_params
    )

    competitor_data_response = competitor_search_executor(params=request_params)
    with open("competitor_data_response.json", "w") as f:
        json.dump(competitor_data_response, f, indent=4)

    if not competitor_data_response["response"]:
        raise ServiceCompetitorSearchError(
            "No response data in competitor search response"
        )

    competitor_details_parsed: CompetitorDetailsParserResponse = (
        CompetitorDetailsParser(response=competitor_data_response["response"]).parse()
    )

    with open("competitor_data_parsed.json", "w") as f:
        json.dump(competitor_details_parsed, f, indent=4)

    competitor_data_mapped = map_hotel_competitor_data(
        competitor_data=competitor_details_parsed["competitor_details_parsed"],
        params=request_params,
    )

    # Deduplicate by provider_id to avoid inserting duplicates for the same lead/provider
    existing_provider_ids = set(
        c.lead_hotel_competitor_data_request_provider_id
        for c in existing_competitor_data
    )
    to_save = [
        c
        for c in competitor_data_mapped
        if c.lead_hotel_competitor_data_request_provider_id not in existing_provider_ids
    ]

    saved_competitors: list[LeadHotelCompetitorData] = []
    if to_save:
        saved_competitors = DatabaseFunctions.save_hotel_competitor_data(
            database_session=database_session, competitor_data=to_save
        )

    # Return the union of existing and newly saved records (all with IDs)
    return [*existing_competitor_data, *saved_competitors]
