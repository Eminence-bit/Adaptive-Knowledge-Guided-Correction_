#!/bin/bash
# AKGC Deployment Script

echo "🚀 Deploying AKGC Algorithm..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python version $python_version is compatible"
else
    echo "❌ Python version $python_version is not compatible. Required: $required_version+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv akgc_env
source akgc_env/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional production dependencies
pip install flask flask-cors gunicorn

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p models/cache
mkdir -p results/comprehensive
mkdir -p logs

# Test the installation
echo "🧪 Testing installation..."
python src/akgc_algorithm.py

if [ $? -eq 0 ]; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    exit 1
fi

# Run comprehensive evaluation
echo "📊 Running comprehensive evaluation..."
python src/comprehensive_evaluation.py --max_samples 100 --output_dir results/comprehensive

# Create production configuration
echo "⚙️ Creating production configuration..."
cat > production_config.yaml << EOF
model: distilbert-base-uncased
cuda: true
sim_threshold: 0.8
hvi_threshold: 0.7
batch_size: 8
api_host: 0.0.0.0
api_port: 5000
max_batch_size: 100
log_level: INFO
EOF

# Create systemd service file
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/akgc.service > /dev/null << EOF
[Unit]
Description=AKGC API Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/akgc_env/bin
ExecStart=$(pwd)/akgc_env/bin/python src/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create Docker configuration
echo "🐳 Creating Docker configuration..."
cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask flask-cors gunicorn

COPY . .

EXPOSE 5000

CMD ["python", "src/api_server.py"]
EOF

# Create docker-compose file
cat > docker-compose.yml << EOF
version: '3.8'

services:
  akgc-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./models/cache:/app/models/cache
      - ./results:/app/results
    restart: unless-stopped
EOF

echo "🎉 Deployment completed successfully!"
echo ""
echo "To start the API server:"
echo "  python src/api_server.py"
echo ""
echo "To start with Docker:"
echo "  docker-compose up -d"
echo ""
echo "To start as a service:"
echo "  sudo systemctl enable akgc"
echo "  sudo systemctl start akgc"
echo ""
echo "API will be available at: http://localhost:5000"
