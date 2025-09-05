BEGIN;

-- 1) lead_hotel_run: add lead_hotel_run_type (NOT NULL)
ALTER TABLE public.lead_hotel_run
  ADD COLUMN lead_hotel_run_type TEXT;

-- Backfill and enforce NOT NULL
UPDATE public.lead_hotel_run
SET lead_hotel_run_type = COALESCE(lead_hotel_run_type, 'HOTEL_ENRICHMENT');

ALTER TABLE public.lead_hotel_run
  ALTER COLUMN lead_hotel_run_type SET NOT NULL;


-- 2) Rename lead_hotel_data -> lead_hotel_mapping_data (structure unchanged)
ALTER TABLE public.lead_hotel_data
  RENAME TO lead_hotel_mapping_data;

-- Rename columns to start with lead_hotel_mapping_data_
ALTER TABLE public.lead_hotel_mapping_data
  RENAME COLUMN lead_id TO lead_hotel_mapping_data_lead_id;
ALTER TABLE public.lead_hotel_mapping_data
  RENAME COLUMN lead_hotel_provider TO lead_hotel_mapping_data_provider;
ALTER TABLE public.lead_hotel_mapping_data
  RENAME COLUMN lead_hotel_property_name TO lead_hotel_mapping_data_property_name;
ALTER TABLE public.lead_hotel_mapping_data
  RENAME COLUMN lead_hotel_property_value TO lead_hotel_mapping_data_property_value;


-- 3) Create lead_hotel_competitor_data (new table)
CREATE TABLE public.lead_hotel_competitor_data (
  lead_hotel_competitor_data_id SERIAL PRIMARY KEY,
  lead_hotel_competitor_lead_id INTEGER NOT NULL REFERENCES public.leads(lead_id),
  lead_hotel_competitor_data_request_provider TEXT NOT NULL,
  lead_hotel_competitor_data_request_provider_id TEXT NOT NULL,
  lead_hotel_competitor_data_request_provider_url TEXT NOT NULL,
  lead_hotel_competitor_data_hotel_name TEXT NOT NULL,
  lead_hotel_competitor_data_hotel_address TEXT,
  lead_hotel_competitor_data_hotel_coordinates DOUBLE PRECISION[],
  lead_hotel_competitor_data_hotel_rating_amount INTEGER,
  lead_hotel_competitor_data_hotel_rating_type TEXT,
  lead_hotel_competitor_data_hotel_review_score DOUBLE PRECISION,
  lead_hotel_competitor_data_hotel_review_count INTEGER,
  lead_hotel_competitor_data_created_at TIMESTAMP NOT NULL
);


-- 4) raw_hotel_data: add new columns and FK
ALTER TABLE public.raw_hotel_data
  ADD COLUMN raw_hotel_data_competitor_data_id INTEGER,
  ADD COLUMN raw_hotel_data_room_name TEXT,
  ADD COLUMN raw_hotel_data_run_type TEXT;

ALTER TABLE public.raw_hotel_data
  ADD CONSTRAINT raw_hotel_data_competitor_data_id_fkey
  FOREIGN KEY (raw_hotel_data_competitor_data_id)
  REFERENCES public.lead_hotel_competitor_data(lead_hotel_competitor_data_id);

-- Backfill and enforce NOT NULL for run type
UPDATE public.raw_hotel_data
SET raw_hotel_data_run_type = COALESCE(raw_hotel_data_run_type, 'HOTEL_ENRICHMENT');

ALTER TABLE public.raw_hotel_data
  ALTER COLUMN raw_hotel_data_run_type SET NOT NULL;

COMMIT;
