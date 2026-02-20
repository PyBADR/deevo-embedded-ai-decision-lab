import streamlit as st
import requests
import os

st.set_page_config(
    page_title="DEEVO Intelligence Lab",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 DEEVO Embedded AI Decision Lab")

st.markdown("""
### Welcome to the Insurance Claims Intelligence Platform

**Powered by AI-Driven Decision Intelligence**

#### 🎯 Production Metrics from GIG Takaful:
- ✅ **8,500+ claims** processed
- ✅ **62% workload reduction** in claims adjudication
- ✅ **8.5M KWD** prevented in fraudulent payouts
- ✅ **<2 seconds** average decision time

---

### 📊 Platform Capabilities:

**1. Claim Scoring** - Instant risk assessment with fraud detection  
**2. KPI Simulation** - Calculate ROI and cost savings  
**3. Governance** - Full audit trail and compliance reporting

Use the sidebar to navigate between different features.

---

### 🔗 System Status
""")

backend_url = os.getenv("FRONTEND_BACKEND_URL", os.getenv("BACKEND_URL", "http://localhost:8000"))

try:
    response = requests.get(f"{backend_url}/health", timeout=5)
    if response.status_code == 200:
        st.success(f"✅ Backend connected: {backend_url}")
    else:
        st.error(f"❌ Backend error: Status {response.status_code}")
except Exception as e:
    st.error(f"❌ Cannot connect to backend: {e}")

st.info("👈 Use the sidebar to access different features")
