"""
Simple FastAPI for Bank Marketing Prediction

Minimal API for demo purposes.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Dict, Any
import pandas as pd
import io
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.model_server import predictor

# Create FastAPI app
app = FastAPI(
    title="Bank Marketing Prediction API",
    description="Simple API for predicting bank marketing campaign outcomes",
    version="1.0.0"
)

# Simple request model with proper type validation
class PredictionRequest(BaseModel):
    """Model for prediction requests with proper field validation."""
    
    # Customer demographics
    age: int
    occupation: str
    marital_status: str
    education: str
    
    # Financial info
    has_credit: str
    housing_loan: str
    personal_loan: str
    
    # Contact details
    contact_mode: str
    month: str
    week_day: str
    last_contact_duration: int
    contacts_per_campaign: int
    N_last_days: int
    nb_previous_contact: int
    previous_outcome: str
    
    # Economic indicators
    emp_var_rate: float
    cons_price_index: float
    cons_conf_index: float
    euri_3_month: float
    nb_employees: float

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Bank Marketing Prediction API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Make a single prediction."""
    try:
        # Convert request to dictionary
        input_data = request.dict()
        
        # Make prediction
        result = predictor.predict(input_data)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):
    """Make batch predictions from CSV file."""
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Make batch predictions
        results_df = predictor.predict_batch(df)
        
        # Convert to JSON-serializable format
        results = results_df.to_dict('records')
        
        return {
            "message": f"Batch prediction completed for {len(results)} samples",
            "total_samples": len(results),
            "predictions": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch prediction: {str(e)}")

@app.get("/sample-csv/download")
async def download_sample_csv():
    """Download a sample CSV file."""
    try:
        # Create sample DataFrame with correct column names for the pipeline
        sample_data = {
            "age": [35, 42, 28],
            "occupation": ["admin.", "management", "student"],
            "marital_status": ["married", "single", "married"],
            "education": ["university.degree", "high.school", "university.degree"],
            "has_credit": ["no", "no", "yes"],
            "housing_loan": ["yes", "no", "yes"],
            "personal_loan": ["no", "yes", "no"],
            "contact_mode": ["cellular", "telephone", "cellular"],
            "month": ["may", "nov", "jul"],
            "week_day": ["thu", "fri", "mon"],
            "last_contact_duration": [261, 151, 198],
            "contacts_per_campaign": [1, 2, 1],
            "N_last_days": [999, 999, 999],
            "nb_previous_contact": [0, 0, 0],
            "previous_outcome": ["nonexistent", "nonexistent", "nonexistent"],
            "emp_var_rate": [1.1, -0.1, 1.4],
            "cons_price_index": [93.994, 93.200, 94.465],
            "cons_conf_index": [-36.4, -42.0, -41.8],
            "euri_3_month": [4.857, 4.191, 4.961],
            "nb_employees": [5191, 5099, 5228]
        }
        
        df = pd.DataFrame(sample_data)
        csv_content = df.to_csv(index=False)
        
        from fastapi.responses import Response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sample_bank_data.csv"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating sample CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
