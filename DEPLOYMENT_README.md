# Enrichment Expedia - GCP Deployment Guide

## 🎉 Deployment Successful!

Your enrichment-expedia application has been successfully deployed to Google Cloud Platform and is running as a systemd service.

## 📊 Deployment Details

- **Instance**: `instance-20250826-072620`
- **Zone**: `us-central1-c`
- **External IP**: `34.60.109.68`
- **Port**: `7890`
- **Service Name**: `enrichment-expedia`

## 🌐 API Endpoints

- **Health Check**: http://34.60.109.68:7890/health
- **API Documentation**: http://34.60.109.68:7890/docs
- **Main Endpoint**: http://34.60.109.68:7890/enrich (POST)

## 🛠️ Useful Commands

### Service Management

```bash
# Check service status
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo systemctl status enrichment-expedia --no-pager"

# View service logs
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo journalctl -u enrichment-expedia -f"

# Stop the service
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo systemctl stop enrichment-expedia"

# Start the service
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo systemctl start enrichment-expedia"

# Restart the service
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo systemctl restart enrichment-expedia"
```

### File Management

```bash
# SSH to the instance
gcloud compute ssh --zone=us-central1-c instance-20250826-072620

# Copy updated files (example)
gcloud compute scp --zone=us-central1-c /path/to/local/file instance-20250826-072620:~/enrichment-expedia-src/target/path
```

### Manual Deployment Script

If you need to redeploy or deploy to a different instance, use:

```bash
./deploy_to_gcp.sh [instance-name] [zone]
```

## 📁 Project Structure on GCP

```
~/enrichment-expedia-src/
├── app/
│   ├── __init__.py
│   ├── processor.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── db_functions.py
│   │   └── connection/
│   │       ├── db_manager.py
│   │       └── connection_monitoring.py
│   └── scrapers/
│       ├── configuration/
│       ├── executors/
│       ├── parsers/
│       ├── services/
│       ├── types/
│       └── utils/
├── debug/
├── venv/
├── entrypoint.py
├── requirements.txt
├── pyproject.toml
└── start_server.sh
```

## 🔧 Configuration

### Environment Variables

The service runs with:

- `PYTHONPATH`: Set to `/home/aleksandarjanca/enrichment-expedia-src`
- Working Directory: `/home/aleksandarjanca/enrichment-expedia-src`

### Systemd Service File

Located at: `/etc/systemd/system/enrichment-expedia.service`

### Firewall Rules

- Rule Name: `enrichment-expedia-port`
- Allowed: `tcp:7890`
- Source: `0.0.0.0/0` (all IPs)

## 🐛 Troubleshooting

### Check if the service is running

```bash
curl -X GET "http://34.60.109.68:7890/health"
```

Expected response: `{"status":"ok"}`

### View logs in real-time

```bash
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo journalctl -u enrichment-expedia -f"
```

### Check virtual environment

```bash
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="cd ~/enrichment-expedia-src && source venv/bin/activate && pip list"
```

### Manual start (for debugging)

```bash
gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="cd ~/enrichment-expedia-src && ./start_server.sh"
```

## 📦 Dependencies Fixed

- **psycopg2 Issue**: Resolved by switching from `psycopg2==2.9.10` to `psycopg2-binary==2.9.10`
- **System Dependencies**: Installed `python3-dev`, `build-essential`, and `libpq-dev`

## 🔄 Updating the Application

To update the application code:

1. **Single File Update**: Use `gcloud compute scp` for individual files
2. **Full Redeployment**: Use the `deploy_to_gcp.sh` script
3. **Restart Service**: Always restart after updates:
   ```bash
   gcloud compute ssh --zone=us-central1-c instance-20250826-072620 --command="sudo systemctl restart enrichment-expedia"
   ```

## 🚨 Important Notes

- The service automatically starts on system boot
- Logs are managed by systemd (use `journalctl` to view)
- The service will automatically restart if it crashes
- Make sure to restart the service after any code changes

## 🧪 Testing the API

### Health Check

```bash
curl -X GET "http://34.60.109.68:7890/health"
```

### API Documentation

Visit: http://34.60.109.68:7890/docs

### Example API Call

```bash
curl -X POST "http://34.60.109.68:7890/enrich" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_hotel_run_id": 123,
    "lead_hotel_run_lead_id": 456,
    "lead_hotel_run_state": "active",
    "lead_hotel_run_request_provider": "expedia",
    "lead_hotel_run_request_provider_id": "hotel_123",
    "lead_hotel_run_request_region": "us-west",
    "lead_hotel_run_request_check_in_date": "2025-10-01T00:00:00",
    "lead_hotel_run_request_length_of_stay": 3,
    "lead_hotel_run_type": "standard",
    "lead_hotel_run_created_at": "2025-09-15T11:00:00"
  }'
```

---

## 🎯 Summary

✅ **Application deployed successfully**
✅ **Service running on port 7890**
✅ **Firewall configured**
✅ **Health endpoint responding**
✅ **API documentation accessible**
✅ **Systemd service configured for auto-start**

Your enrichment-expedia application is now live and ready to process requests!
