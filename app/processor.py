from typing import List
from .db.models import LeadHotelRunModel
from .db.connection.db_manager import create_database_connection
from .types.competitors import CompetitorParams, CompetitorPrice
from .service_competitor_search import service_competitors_search
from .service_competitor_price import service_competitors_price
from .utils.save_to_database import save_to_database

def processor(params : LeadHotelRunModel) -> bool:
    success = True
    all_competitor_prices: List[CompetitorPrice] = []
    database_session = create_database_connection(pool_size=5, max_overflow=10)
    
    try:
        competitors_params = CompetitorParams(
            lead_hotel_run_hotel_id=params.lead_hotel_run_hotel_id,
            lead_hotel_run_provider_hotel_id=params.lead_hotel_run_provider_hotel_id
        )
        
        competitor_data = service_competitors_search(competitor_params=competitors_params, database_session=database_session)
        
        if not competitor_data:
            raise Exception("No competitor data found")
        
        if str(params.lead_hotel_run_type) == "COMPETITOR_ENRICHMENT_PRICE":
            for competitor in competitor_data:
                competitor_prices = service_competitors_price(competitor_data=competitor, params=params)
                if competitor_prices:
                    all_competitor_prices.append(competitor_prices)
                
        successfull_saved = save_to_database(competitor_data=competitor_data, all_competitor_prices=all_competitor_prices, database_session=database_session)
        if not successfull_saved:
            raise Exception("Failed to save competitor data")
    except Exception as e:
        success = False
        print(e)
    
    finally:
        return success