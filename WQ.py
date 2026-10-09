import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="UNZA Water Monitoring System",
    page_icon="💧",
    layout="wide"
)

# ==========================================
# PROTOTYPE SETTINGS
# ==========================================

PH_MIN = 6.5
PH_MAX = 8.5
TURBIDITY_MAX = 5.0
TDS_MAX = 500.0

FLOW_LIMIT = 1.0
PRESSURE_LIMIT = 1.8

# ==========================================
# SESSION HISTORY
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# PAGE TITLE
# ==========================================

st.title("💧 UNZA Water Quality & Leakage Monitoring")
st.write(
    "Monitor water quality and identify possible "
    "pipe leakage in university hostels."
)

st.info(
    "Student prototype: readings are entered manually. "
    "No physical sensors are connected."
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Monitoring Settings")

location = st.sidebar.selectbox(
    "Select monitoring location",
    [
        "Hostel Block A",
        "Hostel Block B",
        "Hostel Block C",
        "Main Water Supply"
    ]
)

# ==========================================
# NUMERIC INPUTS
# ==========================================

st.subheader("Enter Water and Pipe Readings")

col1, col2, col3 = st.columns(3)

with col1:
    ph = st.number_input(
        "pH level",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1,
        format="%.2f"
    )

with col2:
    turbidity = st.number_input(
        "Turbidity (NTU)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )

with col3:
    tds = st.number_input(
        "TDS (ppm)",
        min_value=0.0,
        value=200.0,
        step=1.0,
        format="%.2f"
    )

col4, col5 = st.columns(2)

with col4:
    flow = st.number_input(
        "Flow rate (L/min)",
        min_value=0.0,
        value=0.0,
        step=0.1,
        format="%.2f"
    )

with col5:
    pressure = st.number_input(
        "Water pressure (bar)",
        min_value=0.0,
        value=2.5,
        step=0.1,
        format="%.2f"
    )

# ==========================================
# ANALYSE BUTTON
# ==========================================

if st.button("Analyse and Save Readings", type="primary"):

    alerts = []

    # Check pH
    if ph < PH_MIN or ph > PH_MAX:
        alerts.append(
            f"pH {ph:.2f} is outside the configured "
            f"range of {PH_MIN} to {PH_MAX}."
        )

    # Check turbidity
    if turbidity > TURBIDITY_MAX:
        alerts.append(
            f"High turbidity detected: {turbidity:.2f} NTU."
        )

    # Check total dissolved solids
    if tds > TDS_MAX:
        alerts.append(
            f"TDS exceeds the configured threshold: {tds:.2f} ppm."
        )

    # Check for a possible leak
    if flow > FLOW_LIMIT and pressure < PRESSURE_LIMIT:
        alerts.append(
            "Possible pipe leak: high flow and low pressure "
            "were detected together."
        )

    # Create a monitoring record
    record = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Location": location,
        "pH": ph,
        "Turbidity (NTU)": turbidity,
        "TDS (ppm)": tds,
        "Flow (L/min)": flow,
        "Pressure (bar)": pressure,
        "Status": "ALERT" if alerts else "NORMAL",
        "Alerts": "; ".join(alerts) if alerts else "No configured alerts"
    }

    st.session_state.history.append(record)

    # Display readings
    st.subheader("Current Readings")

    a, b, c = st.columns(3)
    a.metric("pH Level", f"{ph:.2f}")
    b.metric("Turbidity", f"{turbidity:.2f} NTU")
    c.metric("TDS", f"{tds:.2f} ppm")

    d, e = st.columns(2)
    d.metric("Flow Rate", f"{flow:.2f} L/min")
    e.metric("Pressure", f"{pressure:.2f} bar")

    # Display warnings
    st.subheader("Analysis Results")

    if alerts:
        st.error("Warning conditions detected!")

        for alert in alerts:
            st.warning(alert)
    else:
        st.success("No configured warning conditions detected.")

    st.caption(
        "These thresholds are illustrative. A normal result does "
        "not prove that water is safe to drink. Use appropriate "
        "testing and applicable water-quality standards."
    )

# ==========================================
# MONITORING HISTORY
# ==========================================

st.divider()
st.subheader("📊 Monitoring History")

if st.session_state.history:

    df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Water Quality Trends")

    chart_df = df[
        ["pH", "Turbidity (NTU)", "TDS (ppm)"]
    ]

    st.line_chart(chart_df)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Monitoring Records (CSV)",
        data=csv_data,
        file_name="unza_water_records.csv",
        mime="text/csv"
    )

    if st.button("Clear Monitoring History"):
        st.session_state.history = []
        st.rerun()

else:
    st.info(
        "No readings recorded yet. Enter your values and click "
        "'Analyse and Save Readings' to begin."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()
st.caption(
    "UNZA Water Quality & Leakage Monitoring System | "
    "Student software prototype"
)
