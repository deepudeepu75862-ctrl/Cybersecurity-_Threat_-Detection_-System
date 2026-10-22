import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "incidents.db"


def connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def initialize_database():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                failed_attempts INTEGER NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                UNIQUE(timestamp, ip_address, reason)
            )
        """)


def save_incidents(alerts):
    initialize_database()

    with connect() as connection:
        for _, alert in alerts.iterrows():
            connection.execute("""
                INSERT OR IGNORE INTO incidents (
                    timestamp, username, ip_address,
                    failed_attempts, risk_score,
                    risk_level, reason
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(alert["timestamp"]),
                str(alert["username"]),
                str(alert["ip_address"]),
                int(alert["failed_attempts"]),
                int(alert["risk_score"]),
                str(alert["risk_level"]),
                str(alert["reason"])
            ))


def get_incidents():
    initialize_database()

    with connect() as connection:
        return pd.read_sql_query(
            "SELECT * FROM incidents ORDER BY id DESC",
            connection
        )