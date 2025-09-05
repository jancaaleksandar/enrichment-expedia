from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class LeadHotelRunModel(Base):
    __tablename__ = "lead_hotel_run"
    __table_args__ = {"schema": "public"}
    
    lead_hotel_run_id = Column(Integer, primary_key=True, autoincrement=True)
    lead_hotel_run_lead_id = Column(Integer, ForeignKey("public.leads.lead_id"), nullable=False)
    lead_hotel_run_type = Column(String, nullable=False)
    lead_hotel_run_status = Column(String, nullable=False)
    lead_hotel_run_state = Column(String, nullable=False)
    lead_hotel_run_request_provider = Column(String, nullable=False)
    lead_hotel_run_request_provider_id = Column(String, nullable=False)
    lead_hotel_run_request_region = Column(String, nullable=False)
    lead_hotel_run_request_check_in_date = Column(DateTime, nullable=False)
    lead_hotel_run_request_length_of_stay = Column(Integer, nullable=False)
    lead_hotel_run_created_at = Column(DateTime, nullable=False)

class LeadHotelMappingData(Base):
    __tablename__ = "lead_hotel_mapping_data"
    __table_args__ = {"schema" : "public"}
    
    lead_hotel_mapping_data_lead_id = Column(Integer, ForeignKey("public.leads.lead_id"), primary_key=True)
    lead_hotel_mapping_data_provider = Column(String(225), primary_key=True)
    lead_hotel_mapping_data_property_name = Column(String, primary_key=True)
    lead_hotel_mapping_data_property_value = Column(String)
    

class LeadModel(Base):
    __tablename__ = "leads"
    __table_args__ = {"schema" : "public"}
    
    lead_id = Column(Integer, primary_key=True, autoincrement=True)
    lead_country_iso = Column(String, nullable=False)
    lead_domain = Column(String, nullable=True)
    lead_state = Column(String, nullable=False)
    lead_hotel_name = Column(String, nullable=False)
    lead_hotel_address = Column(String, nullable=True)
    lead_hotel_coordinates = Column(ARRAY(Float()), nullable=True)
    lead_hotel_rating_amount = Column(Integer, nullable=True)
    lead_hotel_rating_type = Column(String, nullable=True)
    lead_hotel_review_score = Column(Float(precision=2, asdecimal=False), nullable=True)
    lead_hotel_review_count = Column(Integer, nullable=True)
    
    
class LeadHotelCompetitorData(Base):
    __tablename__ = "lead_hotel_competitor_data"
    __table_args__ = {"schema" : "public"}
    
    lead_hotel_competitor_data_id = Column(Integer, primary_key=True, autoincrement=True)
    lead_hotel_competitor_data_request_provider = Column(String, nullable=False)
    lead_hotel_competitor_data_request_provider_id = Column(String, nullable=False)
    lead_hotel_competitor_data_request_provider_url = Column(String, nullable=False)
    lead_hotel_competitor_data_hotel_name = Column(String, nullable=False)
    lead_hotel_competitor_data_hotel_address = Column(String, nullable=True)
    lead_hotel_competitor_data_hotel_coordinates = Column(ARRAY(Float()), nullable=True)
    lead_hotel_competitor_data_hotel_rating_amount = Column(Integer, nullable=True)
    lead_hotel_competitor_data_hotel_rating_type = Column(String, nullable=True)
    lead_hotel_competitor_data_hotel_review_score = Column(Float(precision=2, asdecimal=False), nullable=True)
    lead_hotel_competitor_data_hotel_review_count = Column(Integer, nullable=True)
    lead_hotel_competitor_data_created_at = Column(DateTime, nullable=False)
    
    
    
class RawHotelData(Base):
    __tablename__ = "raw_hotel_data"
    __table_args__ = {"schema" : "public"}
    
    raw_hotel_data_id = Column(Integer, primary_key=True, autoincrement=True)
    raw_hotel_data_lead_id = Column(Integer, ForeignKey("public.leads.lead_id"), nullable=False)
    raw_hotel_data_run_id = Column(Integer, ForeignKey("public.lead_hotel_run.lead_hotel_run_id"), nullable=False)
    raw_hotel_data_request_provider = Column(String, nullable=False)
    raw_hotel_data_request_provider_id = Column(String, nullable=False)
    raw_hotel_data_request_provider_url = Column(String, nullable=False)
    raw_hotel_data_request_region = Column(String, nullable=False)
    raw_hotel_data_price_check_in_date = Column(DateTime, nullable=False)
    raw_hotel_data_price_sold_out = Column(Boolean, nullable=False)
    raw_hotel_data_price_amount = Column(Float(precision=2, asdecimal=False), nullable=True)
    raw_hotel_data_price_currency = Column(String, nullable=False)
    raw_hotel_data_price_provider = Column(String, nullable=False)
    raw_hotel_data_price_provider_url = Column(String, nullable=False)
    raw_hotel_data_price_provider_icon_url = Column(String, nullable=False)
    raw_hotel_data_price_brand_offer = Column(Boolean, nullable=False)
    raw_hotel_data_competitor_data_id = Column(Integer, ForeignKey("public.lead_hotel_competitor_data.lead_hotel_competitor_data_id"), nullable=True)
    raw_hotel_data_room_name = Column(String, nullable=True)
    raw_hotel_data_run_type = Column(String, nullable=False)
    raw_hotel_data_created_at = Column(DateTime, nullable=False)