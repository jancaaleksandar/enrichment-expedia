from typing import List
from .types.competitors import CompetitorParams, CompetitorData
from sqlalchemy.orm import Session

def service_competitors_search(competitor_params : CompetitorParams, database_session: Session) -> List[CompetitorData]:
    
    #check if the competitors already exist in the database if not run the search process
    
    
    
    return []