import pandas as pd

from src.detector import detect_threats


def test_detects_repeated_failed_logins():
    logs = pd.DataFrame({
        "timestamp": pd.to_datetime([
            "2026-10-22 10:00:00",
            "2026-10-22 10:01:00",
            "2026-10-22 10:02:00",
            "2026-10-22 10:03:00",
            "2026-10-22 10:04:00"
        ]),
        "username": ["bob"] * 5,
        "ip_address": ["203.0.113.20"] * 5,
        "status": ["failed"] * 5
    })

    alerts = detect_threats(logs)

    assert len(alerts) == 1
    assert alerts.iloc[0]["failed_attempts"] == 5
    assert alerts.iloc[0]["risk_level"] == "High"


def test_successful_login_does_not_trigger_alert():
    logs = pd.DataFrame({
        "timestamp": pd.to_datetime(["2026-10-22 10:00:00"]),
        "username": ["alice"],
        "ip_address": ["192.168.1.10"],
        "status": ["success"]
    })

    alerts = detect_threats(logs)

    assert alerts.empty