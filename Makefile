#!/usr/bin/env make
.PHONY: help install start start-api start-app stop clean docker-build docker-run docker-stop

# Default target
help:
	@echo "Bank Marketing Prediction Demo"
	@echo "=============================="
	@echo ""
	@echo "Available commands:"
	@echo "  make start       - Start both API and Streamlit app"
	@echo "  make start-api   - Start only the API server"
	@echo "  make start-app   - Start only the Streamlit app"
	@echo "  make stop        - Stop all running services"
	@echo "  make install     - Install dependencies"
	@echo "  make clean       - Clean up cache files"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run API in Docker container"
	@echo "  make docker-app   - Run Streamlit app in Docker container"
	@echo "  make docker-stop  - Stop Docker container"
	@echo "  make docker-up    - Start both services with docker-compose"
	@echo "  make docker-down  - Stop docker-compose services"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Dependencies installed!"

# Start both services (main command)
start:
	@echo "🚀 Starting Bank Marketing Prediction Demo..."
	@echo ""
	@echo "API will be available at: http://localhost:8000"
	@echo "Streamlit app will be available at: http://localhost:8501"
	@echo "API docs will be available at: http://localhost:8000/docs"
	@echo ""
	@echo "Press Ctrl+C to stop all services"
	@echo ""
	$(MAKE) -j2 start-api-bg start-app-wait

# Start API server only
start-api:
	@echo "🔧 Starting API server..."
	@echo "API will be available at: http://localhost:8000"
	@echo ""
	uv run uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload

# Start Streamlit app only
start-app:
	@echo "🖥️  Starting Streamlit app..."
	@echo "App will be available at: http://localhost:8501"
	@echo ""
	@echo "⚠️  Make sure API is running first!"
	@echo ""
	uv run streamlit run src/app.py --server.port 8501

# Background API start (internal target)
start-api-bg:
	@echo "🔧 Starting API server in background..."
	uv run uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload &

# Start app with delay (internal target)
start-app-wait:
	@echo "⏳ Waiting for API to start..."
	sleep 3
	@echo "🖥️  Starting Streamlit app..."
	uv run streamlit run src/app.py --server.port 8501

# Stop all services
stop:
	@echo "🛑 Stopping all services..."
	pkill -f "uvicorn.*src.api" || true
	pkill -f "streamlit.*src/app.py" || true
	@echo "✅ All services stopped!"

# Clean cache files
clean:
	@echo "🧹 Cleaning up..."
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	@echo "✅ Cleanup complete!"

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t bank-marketing-api .
	@echo "✅ Docker image built!"

docker-run:
	@echo "🐳 Running API in Docker..."
	@echo "API will be available at: http://localhost:8000"
	docker run --rm -p 8000:8000 --name bank-marketing-api bank-marketing-api

docker-app:
	@echo "🐳 Running Streamlit app in Docker..."
	@echo "App will be available at: http://localhost:8501"
	@echo "⚠️  Make sure API is running separately!"
	docker run --rm -p 8501:8501 --name bank-marketing-app -e DOCKER_ENV=true bank-marketing-api \
		uv run streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker stop bank-marketing-api bank-marketing-app || true
	@echo "✅ Docker containers stopped!"

# Docker Compose commands
docker-up:
	@echo "🐳 Starting both services with Docker Compose..."
	@echo "API: http://localhost:8000"
	@echo "App: http://localhost:8501"
	docker compose up --build

docker-down:
	@echo "🛑 Stopping Docker Compose services..."
	docker compose down
	@echo "✅ Services stopped!"
