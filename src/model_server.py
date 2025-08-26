"""
Simple Model Server for Bank Marketing Prediction

Loads and serves predictions from a sklearn pipeline.
"""

import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankMarketingPredictor:
    """Simple predictor using sklearn pipeline."""
    
    def __init__(self, pipeline_path: str = "models/best_rf_pipeline.pkl"):
        """Initialize with the sklearn pipeline."""
        self.pipeline_path = pipeline_path
        self.pipeline = None
        self._load_pipeline()
    
    def _load_pipeline(self):
        """Load the trained sklearn pipeline."""
        try:
            self.pipeline = joblib.load(self.pipeline_path)
            logger.info(f"Pipeline loaded successfully from {self.pipeline_path}")
        except Exception as e:
            logger.error(f"Error loading pipeline: {e}")
            raise
    
    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a prediction on input data."""
        try:
            # Convert input to DataFrame
            df = pd.DataFrame([input_data])
            
            # Make prediction using the pipeline
            prediction = self.pipeline.predict(df)[0]
            prediction_proba = self.pipeline.predict_proba(df)[0]
            
            return {
                "prediction": int(prediction),
                "prediction_label": "yes" if prediction == 1 else "no",
                "probability_no": float(prediction_proba[0]),
                "probability_yes": float(prediction_proba[1]),
                "confidence": float(max(prediction_proba))
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def predict_batch(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """Make predictions on a batch of data."""
        try:
            logger.info(f"Processing batch prediction for {len(input_df)} samples")
            
            # Make predictions using the pipeline
            predictions = self.pipeline.predict(input_df)
            prediction_probas = self.pipeline.predict_proba(input_df)
            
            # Create results DataFrame
            results_df = input_df.copy()
            results_df['prediction'] = predictions
            results_df['prediction_label'] = ['yes' if p == 1 else 'no' for p in predictions]
            results_df['probability_no'] = prediction_probas[:, 0]
            results_df['probability_yes'] = prediction_probas[:, 1]
            results_df['confidence'] = np.max(prediction_probas, axis=1)
            
            logger.info(f"Batch prediction completed successfully")
            return results_df
            
        except Exception as e:
            logger.error(f"Error in batch prediction: {e}")
            raise

# Initialize global predictor instance
predictor = BankMarketingPredictor()
