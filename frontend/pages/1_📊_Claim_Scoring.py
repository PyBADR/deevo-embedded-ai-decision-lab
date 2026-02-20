import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(page_title="Claim Scoring", page_icon="📊", layout="wide")

st.title("📊 Claim Scoring")

backend_url = os.getenv("FRONTEND_BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))

# Input method selection
input_method = st.radio("Input Method", ["Form", "JSON", "Upload File"])

claim_data = None

if input_method == "Form":
    st.subheader("Enter Claim Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        claim_id = st.text_input("Claim ID", value=f"CLM-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
        customer_id = st.text_input("Customer ID", value="CUST-001")
        amount = st.number_input("Claim Amount (KWD)", min_value=0.0, value=5000.0, step=100.0)
    
    with col2:
        incident_type = st.selectbox(
            "Incident Type",
            ["collision", "theft", "fire", "injury", "vandalism", "other"]
        )
        history_score = st.slider("Customer History Score", 0.0, 100.0, 50.0)
    
    claim_data = {
        "claim_id": claim_id,
        "customer_id": customer_id,
        "amount": amount,
        "incident_type": incident_type,
        "history_score": history_score
    }

elif input_method == "JSON":
    st.subheader("Paste JSON")
    json_input = st.text_area(
        "Claim JSON",
        value=json.dumps({
            "claim_id": "CLM-JSON-001",
            "customer_id": "CUST-001",
            "amount": 5000,
            "incident_type": "collision",
            "history_score": 45
        }, indent=2),
        height=200
    )
    
    try:
        claim_data = json.loads(json_input)
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")

else:  # Upload File
    st.subheader("Upload JSON File")
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    
    if uploaded_file is not None:
        try:
            claim_data = json.load(uploaded_file)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON file: {e}")

# Score button
if st.button("🎯 Score Claim", type="primary", use_container_width=True):
    if not claim_data:
        st.error("Please provide claim data")
    else:
        with st.spinner("Scoring claim..."):
            try:
                response = requests.post(
                    f"{backend_url}/api/claim/score",
                    json=claim_data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Claim scored successfully!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Decision", result["decision"])
                    
                    with col2:
                        st.metric("Risk Score", f"{result['risk_score']:.2f}/100")
                    
                    with col3:
                        st.metric("Fraud Probability", f"{result['fraud_probability']:.1%}")
                    
                    # Color-coded decision
                    if result["decision"] == "APPROVE":
                        st.success("✅ **APPROVED** - Auto-process this claim")
                    elif result["decision"] == "REVIEW":
                        st.warning("⚠️ **REVIEW REQUIRED** - Manual adjuster review needed")
                    else:
                        st.error("🚫 **REJECTED** - Escalate to fraud investigation")
                    
                    # Explanation
                    st.subheader("📝 Explanation")
                    st.markdown(result["explanation"])
                    
                    # Business impact
                    st.subheader("💼 Business Impact")
                    if result["decision"] == "APPROVE":
                        st.info("**Time Saved:** ~12 minutes of manual review  \n**Processing:** Fast-track to payment")
                    elif result["decision"] == "REVIEW":
                        st.info("**Action:** Assign to senior adjuster  \n**SLA:** Review within 24 hours")
                    else:
                        st.info("**Action:** Fraud investigation required  \n**Potential Savings:** Prevent fraudulent payout")
                    
                    # Technical details
                    with st.expander("🔍 Technical Details"):
                        st.json({
                            "decision_id": result["decision_id"],
                            "model_version": result["model_version"],
                            "policy_version": result["policy_version"],
                            "timestamp": result["timestamp"]
                        })
                
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.code(response.text)
            
            except Exception as e:
                st.error(f"Request failed: {e}")
