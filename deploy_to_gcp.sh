#!/bin/bash

# GCP Deployment Script for Enrichment Expedia
# This script deploys the enrichment-expedia application to a GCP instance
# Usage: ./deploy_to_gcp.sh [instance-name] [zone]

set -e

# Default values (modify these as needed)
INSTANCE_NAME="${1:-instance-20250826-072620}"
ZONE="${2:-us-central1-c}"
PROJECT_NAME="enrichment-expedia"
REMOTE_DIR="~/${PROJECT_NAME}-src"
LOCAL_PROJECT_DIR="/Users/aleksandarjanca/dev/roompulse/outreach-system/enrichment-expedia"

echo "🚀 Starting deployment to GCP instance: $INSTANCE_NAME in zone: $ZONE"
echo "📁 Local project directory: $LOCAL_PROJECT_DIR"
echo "📁 Remote directory: $REMOTE_DIR"

# Function to copy files to GCP
copy_file() {
    local local_path="$1"
    local remote_path="$2"
    echo "📤 Copying: $local_path -> $remote_path"
    gcloud compute scp --zone="$ZONE" "$local_path" "$INSTANCE_NAME:$remote_path"
}

# Function to copy directories to GCP
copy_directory() {
    local local_path="$1"
    local remote_path="$2"
    echo "📤 Copying directory: $local_path -> $remote_path"
    gcloud compute scp --zone="$ZONE" --recurse "$local_path" "$INSTANCE_NAME:$remote_path"
}

# Function to execute commands on GCP instance
execute_remote() {
    local command="$1"
    echo "🔧 Executing on remote: $command"
    gcloud compute ssh --zone="$ZONE" "$INSTANCE_NAME" --command="$command"
}

echo "📁 Creating remote project directory structure..."
execute_remote "mkdir -p $REMOTE_DIR"
execute_remote "mkdir -p $REMOTE_DIR/app"
execute_remote "mkdir -p $REMOTE_DIR/app/db"
execute_remote "mkdir -p $REMOTE_DIR/app/db/connection"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/configuration"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/executors"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/parsers"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/services"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/types"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/utils"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/utils/common"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/utils/http"
execute_remote "mkdir -p $REMOTE_DIR/app/scrapers/utils/mappers"
execute_remote "mkdir -p $REMOTE_DIR/debug"

echo "📦 Copying Python application files..."

# Copy main application files
copy_file "$LOCAL_PROJECT_DIR/entrypoint.py" "$REMOTE_DIR/entrypoint.py"
copy_file "$LOCAL_PROJECT_DIR/requirements.txt" "$REMOTE_DIR/requirements.txt"
copy_file "$LOCAL_PROJECT_DIR/pyproject.toml" "$REMOTE_DIR/pyproject.toml"

# Copy app directory structure
copy_file "$LOCAL_PROJECT_DIR/app/__init__.py" "$REMOTE_DIR/app/__init__.py"
copy_file "$LOCAL_PROJECT_DIR/app/processor.py" "$REMOTE_DIR/app/processor.py"

# Copy database files
copy_file "$LOCAL_PROJECT_DIR/app/db/__init__.py" "$REMOTE_DIR/app/db/__init__.py"
copy_file "$LOCAL_PROJECT_DIR/app/db/models.py" "$REMOTE_DIR/app/db/models.py"
copy_file "$LOCAL_PROJECT_DIR/app/db/db_functions.py" "$REMOTE_DIR/app/db/db_functions.py"

# Copy database connection files
copy_file "$LOCAL_PROJECT_DIR/app/db/connection/db_manager.py" "$REMOTE_DIR/app/db/connection/db_manager.py"
copy_file "$LOCAL_PROJECT_DIR/app/db/connection/connection_monitoring.py" "$REMOTE_DIR/app/db/connection/connection_monitoring.py"

# Copy scrapers configuration
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/configuration/competitor_search_configuration.py" "$REMOTE_DIR/app/scrapers/configuration/competitor_search_configuration.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/configuration/price_configuration.py" "$REMOTE_DIR/app/scrapers/configuration/price_configuration.py"

# Copy scrapers executors
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/executors/competitor_search_executor.py" "$REMOTE_DIR/app/scrapers/executors/competitor_search_executor.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/executors/price_executor.py" "$REMOTE_DIR/app/scrapers/executors/price_executor.py"

# Copy scrapers parsers
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/parsers/competitor_details_parser.py" "$REMOTE_DIR/app/scrapers/parsers/competitor_details_parser.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/parsers/room_price_parser.py" "$REMOTE_DIR/app/scrapers/parsers/room_price_parser.py"

# Copy scrapers services
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/services/service_competitor_search.py" "$REMOTE_DIR/app/scrapers/services/service_competitor_search.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/services/service_price.py" "$REMOTE_DIR/app/scrapers/services/service_price.py"

# Copy scrapers types
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/types/competitors.py" "$REMOTE_DIR/app/scrapers/types/competitors.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/types/http.py" "$REMOTE_DIR/app/scrapers/types/http.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/types/params.py" "$REMOTE_DIR/app/scrapers/types/params.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/types/provider.py" "$REMOTE_DIR/app/scrapers/types/provider.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/types/room.py" "$REMOTE_DIR/app/scrapers/types/room.py"

# Copy scrapers utils - common
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_calculate_check_out_date.py" "$REMOTE_DIR/app/scrapers/utils/common/common_calculate_check_out_date.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_construct_number_of_nights.py" "$REMOTE_DIR/app/scrapers/utils/common/common_construct_number_of_nights.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_date_to_dict.py" "$REMOTE_DIR/app/scrapers/utils/common/common_date_to_dict.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_date_to_string.py" "$REMOTE_DIR/app/scrapers/utils/common/common_date_to_string.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_get_enviroment.py" "$REMOTE_DIR/app/scrapers/utils/common/common_get_enviroment.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/common_get_proxy_ip.py" "$REMOTE_DIR/app/scrapers/utils/common/common_get_proxy_ip.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/common/construct_url.py" "$REMOTE_DIR/app/scrapers/utils/common/construct_url.py"

# Copy scrapers utils - http
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/http/enums.py" "$REMOTE_DIR/app/scrapers/utils/http/enums.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/http/http_proxy.py" "$REMOTE_DIR/app/scrapers/utils/http/http_proxy.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/http/http_request.py" "$REMOTE_DIR/app/scrapers/utils/http/http_request.py"

# Copy scrapers utils - mappers
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/mappers/map_hotel_competitor_data.py" "$REMOTE_DIR/app/scrapers/utils/mappers/map_hotel_competitor_data.py"
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/mappers/map_raw_hotel_data.py" "$REMOTE_DIR/app/scrapers/utils/mappers/map_raw_hotel_data.py"

# Copy scrapers utils - other
copy_file "$LOCAL_PROJECT_DIR/app/scrapers/utils/save_to_database.py" "$REMOTE_DIR/app/scrapers/utils/save_to_database.py"

echo "🐍 Setting up Python environment on remote instance..."

# Update system and install Python dependencies
execute_remote "sudo apt-get update"
execute_remote "sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential libpq-dev"

# Create virtual environment
execute_remote "cd $REMOTE_DIR && python3 -m venv venv"

# Install Python dependencies
execute_remote "cd $REMOTE_DIR && source venv/bin/activate && pip install --upgrade pip"
execute_remote "cd $REMOTE_DIR && source venv/bin/activate && pip install -r requirements.txt"

echo "🔥 Creating startup script..."
execute_remote "cat > $REMOTE_DIR/start_server.sh << 'EOF'
#!/bin/bash
cd $REMOTE_DIR
source venv/bin/activate
export PYTHONPATH=\$PYTHONPATH:\$(pwd)
python entrypoint.py
EOF"

execute_remote "chmod +x $REMOTE_DIR/start_server.sh"

echo "🔧 Creating systemd service file..."
execute_remote "sudo tee /etc/systemd/system/enrichment-expedia.service > /dev/null << 'EOF'
[Unit]
Description=Enrichment Expedia Service
After=network.target

[Service]
Type=simple
User=\$(whoami)
WorkingDirectory=$REMOTE_DIR
Environment=PYTHONPATH=$REMOTE_DIR
ExecStart=$REMOTE_DIR/venv/bin/python $REMOTE_DIR/entrypoint.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF"

echo "⚡ Enabling and starting the service..."
execute_remote "sudo systemctl daemon-reload"
execute_remote "sudo systemctl enable enrichment-expedia"
execute_remote "sudo systemctl start enrichment-expedia"

echo "📊 Checking service status..."
execute_remote "sudo systemctl status enrichment-expedia --no-pager"

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Useful commands:"
echo "  Check logs: gcloud compute ssh --zone=$ZONE $INSTANCE_NAME --command='sudo journalctl -u enrichment-expedia -f'"
echo "  Stop service: gcloud compute ssh --zone=$ZONE $INSTANCE_NAME --command='sudo systemctl stop enrichment-expedia'"
echo "  Start service: gcloud compute ssh --zone=$ZONE $INSTANCE_NAME --command='sudo systemctl start enrichment-expedia'"
echo "  Restart service: gcloud compute ssh --zone=$ZONE $INSTANCE_NAME --command='sudo systemctl restart enrichment-expedia'"
echo "  SSH to instance: gcloud compute ssh --zone=$ZONE $INSTANCE_NAME"
echo ""
echo "🌐 The service should be running on port 7890"
echo "  Test the API: curl http://[INSTANCE_EXTERNAL_IP]:7890/health"
