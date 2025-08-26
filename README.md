# 🏦 Bank Marketing Prediction Demo

A clean, production-ready ML demo that predicts whether customers will subscribe to bank term deposits. Built with sklearn Random Forest, FastAPI backend, and Streamlit frontend.

## ✨ Features

- **Single Predictions**: Interactive form for individual customer predictions
- **Batch Processing**: Upload CSV files for bulk predictions
- **Clean UI**: Professional Streamlit interface with wide layout
- **REST API**: FastAPI backend with automatic validation
- **Docker Support**: Containerized deployment option
- **Sample Data**: Built-in sample CSV generator

## 🚀 Quick Start

### Local Development
```bash
make start
```

This starts both the API (http://localhost:8000) and Streamlit app (http://localhost:8501).

### Docker Deployment
```bash
make docker-up
```

Both services will be available at the same URLs but running in containers.

## 📁 Project Structure

```
├── src/
│   ├── model_server.py    # ML model wrapper with prediction logic
│   ├── api.py            # FastAPI REST API with validation
│   └── app.py            # Streamlit web interface
├── models/
│   └── best_rf_pipeline.pkl  # Trained Random Forest pipeline
├── data/
│   ├── bank_data_raw.csv     # Original dataset
│   └── sample_data.csv       # Sample for testing
└── Makefile              # Simple automation commands
```

## 🛠️ Commands

### Local Development
- `make start` - Start API + Streamlit app
- `make stop` - Stop all services  
- `make install` - Install Python dependencies

### Docker Options
- `make docker-up` - Start both services in containers
- `make docker-down` - Stop Docker containers
- `make docker-build` - Build Docker images

### Individual Services
- `make start-api` - Start only the API server
- `make start-app` - Start only the Streamlit app

## 🧪 How to Use

1. **Start the application**:
   ```bash
   make start
   ```

2. **Open your browser** to http://localhost:8501

3. **Try single predictions**:
   - Fill out the customer form
   - Click "Make Prediction"
   - See probability scores and confidence

4. **Try batch predictions**:
   - Switch to "Batch Prediction" tab
   - Download sample CSV or upload your own
   - Get results table with download option

## 📊 Model Details

- **Algorithm**: Random Forest Classifier
- **Features**: 20 customer & economic indicators
- **Pipeline**: Includes preprocessing and categorical encoding
- **Output**: Binary prediction (yes/no) with probabilities

## 🔌 API Endpoints

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "occupation": "admin.",
    "month": "may",
    "education": "university.degree",
    "marital_status": "single"
  }'

# Download sample CSV
curl -O http://localhost:8000/sample-csv/download
```

## 🐳 Docker Deployment

The Docker setup creates two services:
- **api**: FastAPI backend (internal port 8000)
- **app**: Streamlit frontend (internal port 8501)

Both services communicate through Docker's internal network, with automatic service discovery.

## 💡 Technical Notes

- Built with `uv` for fast Python package management
- Environment-aware API URL detection (local vs Docker)
- Categorical validation prevents unknown category errors
- Wide Streamlit layout for better user experience
