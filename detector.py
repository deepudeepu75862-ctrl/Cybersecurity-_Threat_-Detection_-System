from pathlib import Path
import pandas as pd
import ipaddress

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / ".vscode" / "data" / "sample_logs.csv"

WINDOW_MINUTES = 5
FAILED_THRESHOLD = 5


def load_logs():
    df = pd.read_csv(LOG_FILE)

    required = {"timestamp", "username", "ip_address", "status"}

    if not required.issubset(df.columns):
        raise ValueError("CSV columns are missing")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )
    df["username"] = df["username"].astype("string").str.strip()
    df["ip_address"] = df["ip_address"].astype("string").str.strip()
    df["status"] = (
        df["status"].astype("string").str.strip().str.lower()
    )

    df = df.dropna(
        subset=["timestamp", "username", "ip_address", "status"]
    )
    df = df[df["status"].isin(["success", "failed"])]

    def valid_ip(value):
        try:
            ipaddress.ip_address(str(value))
            return True
        except ValueError:
            return False

    df = df[df["ip_address"].map(valid_ip)]

    return df.sort_values("timestamp").reset_index(drop=True)


def detect_threats(df):
    columns = [
        "timestamp", "username", "ip_address",
        "failed_attempts", "risk_score", "risk_level", "reason"
    ]

    alerts = []

    if df.empty:
        return pd.DataFrame(columns=columns)

    failed = df[df["status"] == "failed"].copy()

    for ip, group in failed.groupby("ip_address"):
        group = group.sort_values("timestamp").reset_index(drop=True)
        left = 0

        for right in range(len(group)):
            while (
                group.loc[right, "timestamp"]
                - group.loc[left, "timestamp"]
            ).total_seconds() > WINDOW_MINUTES * 60:
                left += 1

            attempts = right - left + 1

            if attempts >= FAILED_THRESHOLD:
                window = group.iloc[left:right + 1]
                score = min(100, 70 + (attempts - 5) * 10)

                alerts.append({
                    "timestamp": group.loc[right, "timestamp"],
                    "username": ", ".join(
                        sorted(window["username"].unique())
                    ),
                    "ip_address": ip,
                    "failed_attempts": attempts,
                    "risk_score": score,
                    "risk_level": "High" if score >= 70 else "Medium",
                    "reason": f"{attempts} failed logins within 5 minutes"
                })

                break

    return pd.DataFrame(alerts, columns=columns)


if __name__ == "__main__":
    logs = load_logs()
    alerts = detect_threats(logs)

    print("Total log events:", len(logs))
    print("Suspicious IP addresses:", len(alerts))
    print(alerts.to_string(index=False))