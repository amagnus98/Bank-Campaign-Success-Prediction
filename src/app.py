"""
Simple Streamlit App for Bank Marketing Prediction

Clean demo interface with minimal complexity.
"""

import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any
import os

# Configuration - detect if running in Docker
if os.getenv('DOCKER_ENV'):
    if os.getenv('COMPOSE_ENV'):
        API_BASE_URL = "http://api:8000"  # Docker Compose internal network
    else:
        API_BASE_URL = "http://host.docker.internal:8000"  # Docker Desktop
else:
    API_BASE_URL = "http://localhost:8000"  # Local development

def call_prediction_api(data: Dict[str, Any]) -> Dict[str, Any]:
    """Call the API for prediction."""
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        st.error(f"Response status: {getattr(e.response, 'status_code', 'No response')}")
        st.error(f"Response text: {getattr(e.response, 'text', 'No response text')}")
        return None

def check_api_health() -> bool:
    """Check if API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except:
        return False

def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Bank Marketing Prediction",
        page_icon="🏦",
        layout="wide"
    )
    
    # Add CSS for full width
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 100% !important;
            padding-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🏦 Bank Marketing Prediction Demo")
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ API is not running. Please start it with: make start-api")
        return
    
    st.success("✅ API is ready!")
    
    # Create tabs
    tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])
    
    with tab1:
        single_prediction_interface()
    
    with tab2:
        batch_prediction_interface()

def single_prediction_interface():
    """Simple single prediction interface."""
    st.header("Make a Prediction")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Customer Information")
        
        age = st.number_input("Age", min_value=18, max_value=95, value=35)
        
        job = st.selectbox("Job", [
            "admin.", "blue-collar", "entrepreneur", "housemaid", "management", 
            "retired", "self-employed", "services", "student", "technician", 
            "unemployed", "unknown"
        ])
        
        marital_status = st.selectbox("Marital Status", ["divorced", "married", "single", "unknown"])
        
        education = st.selectbox("Education", [
            "basic.4y", "basic.6y", "basic.9y", "high.school", "illiterate", 
            "professional.course", "university.degree", "unknown"
        ])
        
        has_credit = st.selectbox("Has Credit in Default?", ["no", "yes", "unknown"])
        housing_loan = st.selectbox("Has Housing Loan?", ["no", "yes", "unknown"])
        personal_loan = st.selectbox("Has Personal Loan?", ["no", "yes", "unknown"])
    
    with col2:
        st.subheader("Contact & Campaign")
        
        contact_mode = st.selectbox("Contact Type", ["cellular", "telephone"])
        
        month = st.selectbox("Last Contact Month", [
            "mar", "apr", "may", "jun", "jul", "aug", 
            "sep", "oct", "nov", "dec"
        ])
        
        week_day = st.selectbox("Day of Week", [
            "mon", "tue", "wed", "thu", "fri"
        ])
        
        last_contact_duration = st.number_input("Contact Duration (seconds)", min_value=0, value=200)
        contacts_per_campaign = st.number_input("Campaign Contacts", min_value=1, value=1)
        N_last_days = st.number_input("Days Since Previous Contact", min_value=0, value=999)
        nb_previous_contact = st.number_input("Previous Contacts", min_value=0, value=0)
        previous_outcome = st.selectbox("Previous Outcome", ["failure", "nonexistent", "success"])
    
    # Economic indicators in a separate section
    st.subheader("Economic Context")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        emp_var_rate = st.number_input("Employment Variation Rate", value=1.1, step=0.1)
        cons_price_index = st.number_input("Consumer Price Index", value=93.994, step=0.001)
    
    with col4:
        cons_conf_index = st.number_input("Consumer Confidence Index", value=-36.4, step=0.1)
        euri_3_month = st.number_input("Euribor 3M Rate", value=4.857, step=0.001)
    
    with col5:
        nb_employees = st.number_input("Number Employed", value=5191.0, step=0.1)
    
    # Predict button
    if st.button("🔮 Make Prediction", type="primary"):
        # Prepare data using correct column names for the pipeline
        input_data = {
            "age": age,
            "occupation": job,
            "marital_status": marital_status,
            "education": education,
            "has_credit": has_credit,
            "housing_loan": housing_loan,
            "personal_loan": personal_loan,
            "contact_mode": contact_mode,
            "month": month,
            "week_day": week_day,
            "last_contact_duration": last_contact_duration,
            "contacts_per_campaign": contacts_per_campaign,
            "N_last_days": N_last_days,
            "nb_previous_contact": nb_previous_contact,
            "previous_outcome": previous_outcome,
            "emp_var_rate": emp_var_rate,
            "cons_price_index": cons_price_index,
            "cons_conf_index": cons_conf_index,
            "euri_3_month": euri_3_month,
            "nb_employees": nb_employees
        }
        
        with st.spinner("Making prediction..."):
            result = call_prediction_api(input_data)
        
        if result:
            display_single_prediction_result(result)

def batch_prediction_interface():
    """Simple batch prediction interface."""
    st.header("Batch Prediction from CSV")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload CSV with bank marketing data"
        )
    
    with col2:
        if st.button("📋 Download Sample", type="secondary"):
            try:
                response = requests.get(f"{API_BASE_URL}/sample-csv/download")
                if response.status_code == 200:
                    st.download_button(
                        label="💾 sample_data.csv",
                        data=response.content,
                        file_name="sample_bank_data.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Error downloading sample: {e}")
    
    if uploaded_file is not None:
        # Show preview
        try:
            df_preview = pd.read_csv(uploaded_file)
            st.subheader("📊 Data Preview")
            st.dataframe(df_preview.head(), use_container_width=True)
            st.write(f"Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")
            
            uploaded_file.seek(0)  # Reset file pointer
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return
        
        # Predict button
        if st.button("🚀 Run Batch Prediction", type="primary"):
            with st.spinner("Processing..."):
                results = call_batch_prediction_api(uploaded_file)
            
            if results:
                display_batch_prediction_results(results)

def display_single_prediction_result(result):
    """Display single prediction result."""
    st.markdown("---")
    st.subheader("🎯 Prediction Result")
    
    prediction_label = result.get('prediction_label', 'Unknown')
    confidence = result.get('confidence', 0)
    prob_yes = result.get('probability_yes', 0)
    prob_no = result.get('probability_no', 0)
    
    # Main result
    if prediction_label == 'yes':
        st.success(f"✅ **{prediction_label.upper()}** - Customer likely to subscribe!")
    else:
        st.error(f"❌ **{prediction_label.upper()}** - Customer unlikely to subscribe")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Probability (Yes)", f"{prob_yes:.1%}")
    with col2:
        st.metric("Probability (No)", f"{prob_no:.1%}")
    with col3:
        st.metric("Confidence", f"{confidence:.1%}")

def display_batch_prediction_results(results):
    """Display batch prediction results."""
    if results and 'predictions' in results:
        predictions_df = pd.DataFrame(results['predictions'])
        
        st.success(f"✅ Processed {results['total_samples']} samples")
        
        # Quick stats
        total_yes = sum(1 for p in predictions_df['prediction_label'] if p == 'yes')
        total_no = len(predictions_df) - total_yes
        avg_confidence = predictions_df['confidence'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", len(predictions_df))
        with col2:
            st.metric("Predicted 'Yes'", total_yes)
        with col3:
            st.metric("Predicted 'No'", total_no)
        with col4:
            st.metric("Avg Confidence", f"{avg_confidence:.1%}")
        
        st.markdown("---")
        st.subheader("📋 Results")
        
        # Clean results table
        display_df = predictions_df[['prediction_label', 'probability_yes', 'probability_no', 'confidence']].copy()
        display_df.index = range(1, len(display_df) + 1)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "prediction_label": st.column_config.TextColumn("Prediction"),
                "probability_yes": st.column_config.ProgressColumn(
                    "Prob (Yes)", min_value=0, max_value=1, format="%.1%"
                ),
                "probability_no": st.column_config.ProgressColumn(
                    "Prob (No)", min_value=0, max_value=1, format="%.1%"
                ),
                "confidence": st.column_config.ProgressColumn(
                    "Confidence", min_value=0, max_value=1, format="%.1%"
                )
            }
        )
        
        # Download results
        st.markdown("---")
        csv_results = predictions_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results",
            data=csv_results,
            file_name="predictions.csv",
            mime="text/csv",
            type="primary"
        )

def call_batch_prediction_api(uploaded_file):
    """Call batch prediction API."""
    try:
        uploaded_file.seek(0)
        files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
        response = requests.post(f"{API_BASE_URL}/predict/batch", files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return None

if __name__ == "__main__":
    main()
