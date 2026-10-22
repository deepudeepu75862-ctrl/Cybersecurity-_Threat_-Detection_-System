🛡️ AI-Powered Cybersecurity Threat Detection System

📌 Overview

The AI-Powered Cybersecurity Threat Detection System is a Python-based project that analyzes login activity to identify suspicious behavior. It detects repeated failed login attempts, calculates risk scores, uses machine learning to identify anomalies, and displays security information through an interactive dashboard.

✨ Features

- 🔍 Detect repeated failed login attempts within five minutes.
- 🚨 Generate alerts for suspicious login activity.
- 📊 Calculate risk scores from 0 to 100.
- 🤖 Use Isolation Forest for anomaly detection.
- 🗄️ Store security incidents using SQLite.
- 📈 Display login statistics and charts.
- 📥 Export security alerts as CSV files.
- 🧪 Test detection logic using Pytest.

🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- Isolation Forest
- SQLite
- Streamlit
- Plotly
- Pytest

📁 Project Structure

cybersecurity-threat-detection/
├── data/
│   └── sample_logs.csv
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── detector.py
│   ├── database.py
│   └── ml_model.py
├── tests/
│   └── test_detector.py
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation

1. Install Python

Install Python 3.12 or a compatible version.

2. Clone the repository

git clone https://github.com/YOUR-USERNAME/cybersecurity-threat-detection.git

Replace "YOUR-USERNAME" with your GitHub username.

3. Open the project folder

cd cybersecurity-threat-detection

4. Create a virtual environment

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

5. Install dependencies

python -m pip install -r requirements.txt

▶️ How to Run

Run the detection engine

python -m src.detector

Launch the dashboard

python -m streamlit run src/app.py

Open the local URL displayed in the terminal, usually "http://localhost:8501".

🧪 Run Tests

python -m pytest -v

📊 Dataset

The project uses simulated login records containing timestamps, usernames, IP addresses, and login statuses. The sample data demonstrates how repeated failed login attempts can trigger a security alert.

⚠️ Limitations

- The project analyzes sample login logs rather than monitoring live network traffic.
- Repeated failed logins do not necessarily indicate an attack.
- Machine-learning predictions depend on the quality and size of the dataset.
- Alerts require further investigation and do not confirm malicious activity.

🔮 Future Improvements

- Integrate larger security datasets.
- Add real-time log monitoring for authorized systems.
- Improve anomaly detection and model evaluation.
- Add alert notifications and incident management.
- Enhance dashboard filtering and reporting.

👩‍💻 Author

Your Name

GitHub: Add your GitHub profile link here.

📜 Disclaimer

This project is intended for educational and defensive cybersecurity purposes. It uses simulated login data and should not be treated as a production security monitoring system.
