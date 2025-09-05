from typing import List
from sqlalchemy.orm import Session
from ..db.saving_functions import DatabaseSavingFunctions
from ..types.competitors import CompetitorData, CompetitorPrice
from ..utils.mappers.map_hotel_competitor_data import map_hotel_competitor_data


def save_to_database(competitor_data: List[CompetitorData], all_competitor_prices: List[CompetitorPrice], database_session: Session) -> bool:
    success = False
    
    try:
        
        competitor_data_to_save = map_hotel_competitor_data(competitor_data=competitor_data)
        if not competitor_data_to_save:
            raise Exception("Failed to map competitor data")
        
        for competitor in competitor_data_to_save:
            competitor_data_saved_successfully = DatabaseSavingFunctions.save_hotel_competitor_data(competitor_data=competitor, database_session=database_session)
        
        if not competitor_data_saved_successfully:
            raise Exception("Failed to save competitor data")
        
        if all_competitor_prices: 
            for competitor in competitor_data_to_save:
                saved_successfully = DatabaseSavingFunctions.save_hotel_competitor_data(competitor_data=competitor, all_competitor_prices=all_competitor_prices, database_session=database_session)
                if not saved_successfully:
                    raise Exception("Failed to save competitor data")
        
        return True
    except Exception as e:
        success = False
        print(e)
        
    finally:
        return success