from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models import LeadHotelRunModel

from ..db.models import LeadHotelCompetitorData, RawHotelData


class DatabaseFunctions:
    @staticmethod
    def update_lead_hotel_run(
        session: Session,
        lead_hotel_run_id: int,
        status: Optional[str] = None,
        state: Optional[str] = None,
    ) -> bool:
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

    @staticmethod
    def get_hotel_competitor_data(
        database_session: Session, request_params: LeadHotelRunModel
    ) -> List[LeadHotelCompetitorData]:
        """
        Get hotel competitor data filtering by lead ID and provider.

        Args:
            database_session: SQLAlchemy session
            request_params: LeadHotelRunModel containing lead_id and provider info

        Returns:
            List of competitor data matching the lead ID and provider
        """
        return (
            database_session.query(LeadHotelCompetitorData)
            .filter(
                LeadHotelCompetitorData.lead_hotel_competitor_lead_id
                == request_params.lead_hotel_run_lead_id,
                LeadHotelCompetitorData.lead_hotel_competitor_data_request_provider
                == request_params.lead_hotel_run_request_provider,
            )
            .all()
        )

    @staticmethod
    def save_hotel_competitor_data(
        database_session: Session,
        competitor_data: List[LeadHotelCompetitorData],
    ) -> List[LeadHotelCompetitorData]:
        database_session.add_all(competitor_data)
        database_session.commit()
        # Refresh all objects to get their database-assigned IDs and any other DB-generated values
        for item in competitor_data:
            database_session.refresh(item)
        return competitor_data

    @staticmethod
    def save_raw_hotel_data(
        database_session: Session, raw_hotel_data: List[RawHotelData]
    ) -> bool:
        database_session.add_all(raw_hotel_data)
        database_session.commit()
        return True
