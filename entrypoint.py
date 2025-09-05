import socket
import os
from typing import Any, Dict, Optional
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.processor import processor
from app.db.models import LeadHotelRunModel


app = FastAPI(title="Leads Booking API", version="0.1.0")


class LeadHotelRunRequest(BaseModel):
    lead_hotel_run_id: int
    lead_hotel_run_lead_id: int
    lead_hotel_run_status: Optional[str] = None
    lead_hotel_run_state: str
    lead_hotel_run_request_provider: str
    lead_hotel_run_request_provider_id: str
    lead_hotel_run_request_region: str
    lead_hotel_run_request_check_in_date: str  # Will convert to datetime
    lead_hotel_run_request_length_of_stay: int
    lead_hotel_run_type: str
    lead_hotel_run_created_at: str  # Will convert to datetime


@app.get("/health", tags=["system"])
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/enrich", status_code=202, tags=["enrich"])
async def ingest_event(request: LeadHotelRunRequest) -> Any:
    if not request.lead_hotel_run_id:
        raise HTTPException(status_code=400, detail="lead_hotel_run_id is required")
    
    # Convert Pydantic model to SQLAlchemy model
    model = LeadHotelRunModel(
        lead_hotel_run_id=request.lead_hotel_run_id,
        lead_hotel_run_lead_id=request.lead_hotel_run_lead_id,
        lead_hotel_run_status=request.lead_hotel_run_status,
        lead_hotel_run_state=request.lead_hotel_run_state,
        lead_hotel_run_request_provider=request.lead_hotel_run_request_provider,
        lead_hotel_run_request_provider_id=request.lead_hotel_run_request_provider_id,
        lead_hotel_run_request_region=request.lead_hotel_run_request_region,
        lead_hotel_run_request_check_in_date=datetime.fromisoformat(request.lead_hotel_run_request_check_in_date),
        lead_hotel_run_request_length_of_stay=request.lead_hotel_run_request_length_of_stay,
        lead_hotel_run_type=request.lead_hotel_run_type,
        lead_hotel_run_created_at=datetime.fromisoformat(request.lead_hotel_run_created_at)
    )
    
    response = processor(model)
    
    # Create debug directory if it doesn't exist
    os.makedirs("debug", exist_ok=True)
    return response


def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    host_ip = get_local_ip()
    print(f"Starting server on {host_ip}:7890")
    uvicorn.run("entrypoint:app", host="0.0.0.0", port=7890, reload=True) # type: ignore