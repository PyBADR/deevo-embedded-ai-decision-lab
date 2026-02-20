import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Governance", page_icon="🔍", layout="wide")

st.title("🔍 Governance & Audit Trail")

backend_url = os.getenv("FRONTEND_BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))

# Fetch decisions
st.subheader("📋 Recent Decisions")

limit = st.slider("Number of records", 10, 200, 50, 10)

if st.button("🔄 Refresh Data", type="primary"):
    with st.spinner("Loading decisions..."):
        try:
            response = requests.get(
                f"{backend_url}/api/decisions",
                params={"limit": limit},
                timeout=10
            )
            
            if response.status_code == 200:
                decisions = response.json()
                
                if decisions:
                    # Convert to DataFrame
                    df = pd.DataFrame(decisions)
                    
                    # Format timestamp
                    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Decisions", len(df))
                    
                    with col2:
                        approved = len(df[df['decision'] == 'APPROVE'])
                        st.metric("Approved", approved)
                    
                    with col3:
                        review = len(df[df['decision'] == 'REVIEW'])
                        st.metric("Review", review)
                    
                    with col4:
                        rejected = len(df[df['decision'] == 'REJECT'])
                        st.metric("Rejected", rejected)
                    
                    # Display table
                    st.dataframe(
                        df[['claim_id', 'customer_id', 'decision', 'risk_score', 'fraud_probability', 'timestamp']],
                        use_container_width=True
                    )
                    
                    # Export button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"decisions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Decision detail viewer
                    st.subheader("🔎 Decision Detail")
                    
                    selected_decision = st.selectbox(
                        "Select Decision to View",
                        options=df['decision_id'].tolist(),
                        format_func=lambda x: f"{df[df['decision_id']==x]['claim_id'].values[0]} - {x}"
                    )
                    
                    if selected_decision:
                        detail_response = requests.get(
                            f"{backend_url}/api/decisions/{selected_decision}",
                            timeout=10
                        )
                        
                        if detail_response.status_code == 200:
                            detail = detail_response.json()
                            
                            # Decision info
                            st.json(detail['decision'])
                            
                            # Audit trail
                            st.subheader("📜 Audit Trail")
                            
                            if detail['audit_events']:
                                for event in detail['audit_events']:
                                    with st.expander(f"{event['event_type']} - {event['created_at']}"):
                                        st.json(event['event_payload'])
                            else:
                                st.info("No audit events found")
                        else:
                            st.error(f"Failed to load detail: {detail_response.status_code}")
                else:
                    st.warning("No decisions found")
            else:
                st.error(f"API Error: {response.status_code}")
        
        except Exception as e:
            st.error(f"Request failed: {e}")
