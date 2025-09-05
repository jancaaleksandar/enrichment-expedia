from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import LeadHotelRunModel


class DatabaseSavingFunctions:
    @staticmethod
    def update_lead_hotel_run(session: Session,lead_hotel_run_id: int,status: Optional[str] = None,state: Optional[str] = None) -> bool:
        updates: Dict[Any, Any] = {}
        if status is not None:
            updates[LeadHotelRunModel.lead_hotel_run_status] = status
        if state is not None:
            updates[LeadHotelRunModel.lead_hotel_run_state] = state

        if not updates:
            return False
        updated_rows = (
            session.query(LeadHotelRunModel)
            .filter(LeadHotelRunModel.lead_hotel_run_id == lead_hotel_run_id)
            .update(updates, synchronize_session=False)
        )
        session.commit()
        return updated_rows > 0