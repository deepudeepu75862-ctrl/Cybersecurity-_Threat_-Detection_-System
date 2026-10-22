import streamlit as st
import plotly.express as px

from src.detector import load_logs, detect_threats
from src.database import save_incidents, get_incidents
from src.ml_model import add_anomaly_predictions

st.set_page_config(
    page_title="Cybersecurity Threat Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI-Powered Cybersecurity Threat Detection")
st.caption("Analyze login events and identify suspicious activity.")

try:
    logs = load_logs()
    alerts = detect_threats(logs)
    save_incidents(alerts)
    analyzed_logs = add_anomaly_predictions(logs)

except (OSError, ValueError, KeyError) as error:
    st.error(f"Error processing data: {error}")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", len(logs))
col2.metric("Failed Logins", int((logs["status"] == "failed").sum()))
col3.metric("Suspicious IPs", alerts["ip_address"].nunique())
col4.metric(
    "Anomalous Events",
    int((analyzed_logs["anomaly"] == "Anomaly").sum())
)

st.subheader("Login Activity")

activity = (
    logs["status"]
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Count")
)

fig = px.bar(
    activity,
    x="Status",
    y="Count",
    color="Status",
    title="Successful vs Failed Logins"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Security Alerts")

if alerts.empty:
    st.success("No repeated-login alerts detected.")
else:
    st.dataframe(alerts, use_container_width=True)

    st.download_button(
        "Download Alerts CSV",
        data=alerts.to_csv(index=False).encode("utf-8"),
        file_name="security_alerts.csv",
        mime="text/csv"
    )

st.subheader("Machine Learning Results")
st.dataframe(analyzed_logs, use_container_width=True)

st.subheader("Incident History")
st.dataframe(get_incidents(), use_container_width=True)