from typing import List

from .db.connection.db_manager import create_database_connection
from .db.db_functions import DatabaseFunctions
from .db.models import LeadHotelRunModel
from .scrapers.services.service_competitor_search import service_competitors_search
from .scrapers.services.service_price import service_price
from .scrapers.types.room import RoomDetails
from .scrapers.utils.mappers.map_raw_hotel_data import map_raw_hotel_data


def processor(params: LeadHotelRunModel) -> bool:
    database_session = create_database_connection(pool_size=5, max_overflow=10)
    try:
        # Get competitor data
        competitor_response = service_competitors_search(
            request_params=params, database_session=database_session
        )
        if not competitor_response:
            raise Exception("No competitor data found")

        competitors_data = competitor_response
        if not competitors_data:
            raise Exception("No competitor details found in response")

        all_competitor_prices: List[RoomDetails] = []
        if str(params.lead_hotel_run_type) == "COMPETITOR_ENRICHMENT_PRICE":
            # os.makedirs("debug", exist_ok=True)
            # serializable_competitors = [
            #     {
            #         "lead_hotel_competitor_data_id": competitor.lead_hotel_competitor_data_id,
            #         "lead_hotel_competitor_data_request_provider_id": competitor.lead_hotel_competitor_data_request_provider_id,
            #         "lead_hotel_competitor_data_request_provider_url": competitor.lead_hotel_competitor_data_request_provider_url,
            #         "lead_hotel_competitor_data_hotel_name": competitor.lead_hotel_competitor_data_hotel_name,
            #     }
            #     for competitor in competitors_data
            # ]
            # with open("debug/competitor_data.json", "w") as f:
            #     json.dump(serializable_competitors, f, indent=4)
            for competitor in competitors_data:
                competitor_params = LeadHotelRunModel(
                    lead_hotel_run_id=params.lead_hotel_run_id,
                    lead_hotel_run_lead_id=params.lead_hotel_run_lead_id,
                    lead_hotel_run_type=params.lead_hotel_run_type,
                    lead_hotel_run_status=params.lead_hotel_run_status,
                    lead_hotel_run_state=params.lead_hotel_run_state,
                    lead_hotel_run_request_provider=params.lead_hotel_run_request_provider,
                    lead_hotel_run_request_provider_id=competitor.lead_hotel_competitor_data_request_provider_id,
                    lead_hotel_run_request_region=params.lead_hotel_run_request_region,
                    lead_hotel_run_request_check_in_date=params.lead_hotel_run_request_check_in_date,
                    lead_hotel_run_request_length_of_stay=params.lead_hotel_run_request_length_of_stay,
                    lead_hotel_run_created_at=params.lead_hotel_run_created_at,
                )

                offer_room_details = service_price(
                    params=competitor_params,
                    competitor_data_id=competitor.lead_hotel_competitor_data_id,
                )
                if offer_room_details is not None:
                    all_competitor_prices.append(offer_room_details)
                else:
                    raise Exception("No price data found for competitor")

        raw_hotel_data_mapped = map_raw_hotel_data(
            room_offer_details=all_competitor_prices, params=params
        )
        raw_hotel_data_saved = DatabaseFunctions.save_raw_hotel_data(
            raw_hotel_data=raw_hotel_data_mapped, database_session=database_session
        )

        if not raw_hotel_data_saved:
            raise Exception("Failed to save raw hotel data")

        return True

    except Exception as e:
        print(f"Error in processor: {str(e)}")
        return False
