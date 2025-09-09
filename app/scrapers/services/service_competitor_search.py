import json
from typing import List

from sqlalchemy.orm import Session

from ...db.db_functions import DatabaseFunctions
from ...db.models import LeadHotelCompetitorData, LeadHotelRunModel
from ..executors.competitor_search_executor import competitor_search_executor
from ..parsers.competitor_details_parser import (
    CompetitorDetailsParser,
    CompetitorDetailsParserResponse,
)
from ..utils.mappers.map_hotel_competitor_data import map_hotel_competitor_data


def service_competitors_search(
    request_params: LeadHotelRunModel, database_session: Session
) -> List[LeadHotelCompetitorData]:

    competitor_data_in_database = DatabaseFunctions.get_hotel_competitor_data(
        database_session=database_session, request_params=request_params
    )

    if competitor_data_in_database:
        return competitor_data_in_database

    competitor_data_response = competitor_search_executor(params=request_params)
    with open("competitor_data_response.json", "w") as f:
        json.dump(competitor_data_response, f, indent=4)

    competitor_details_parsed: CompetitorDetailsParserResponse = (
        CompetitorDetailsParser(response=competitor_data_response["response"]).parse()
    )

    with open("competitor_data_parsed.json", "w") as f:
        json.dump(competitor_details_parsed, f, indent=4)

    competitor_data_mapped = map_hotel_competitor_data(
        competitor_data=competitor_details_parsed, params=request_params
    )

    competitor_data_saved = DatabaseFunctions.save_hotel_competitor_data(
        competitor_data=competitor_data_mapped, database_session=database_session
    )

    # * we are returning the saved object that was refreshed by the function so we can use the competitor_data_id later
    return competitor_data_saved
