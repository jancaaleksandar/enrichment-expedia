from datetime import datetime

from app.db.models import LeadHotelRunModel
from app.processor import processor

params: LeadHotelRunModel = LeadHotelRunModel(
    lead_hotel_run_id=1,
    lead_hotel_run_lead_id=1,
    lead_hotel_run_status=None,
    lead_hotel_run_state="NEW",
    lead_hotel_run_request_provider="EXPEDIA",
    lead_hotel_run_request_provider_id="38235667",
    lead_hotel_run_request_region="EUROPE",
    # Use a real date object instead of a string
    lead_hotel_run_request_check_in_date=datetime(2025, 10, 14).date(),
    lead_hotel_run_request_length_of_stay=1,
    lead_hotel_run_type="COMPETITOR_ENRICHMENT_PRICE",
    # Use a real datetime instead of a string
    lead_hotel_run_created_at=datetime(2025, 8, 2, 12, 0, 0),
)

status = processor(params)
print(status)
