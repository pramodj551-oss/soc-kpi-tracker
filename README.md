# 📊 Automated Security KPI & Metrics Tracker

**Author:** Pramod Prakash Jadhav  
**GitHub:** [github.com/pramodj551-oss](https://github.com/pramodj551-oss)  
**LinkedIn:** [linkedin.com/in/pramod-jadhav-42ba2281](https://linkedin.com/in/pramod-jadhav-42ba2281)

**streamliit:** [https://soc-kpi-tracker-gjxmd4wqg556mb2xmxacnr.streamlit.app/](https://soc-kpi-tracker-gjxmd4wqg556mb2xmxacnr.streamlit.app/)

---

## 📌 Problem

In my SOC role, **generating the weekly performance report took 4+ hours** of manual work — pulling numbers from SIEM, calculating KPIs, formatting spreadsheets, and emailing summaries.

It was error-prone and left managers waiting for critical metrics.

## 💡 Solution

Built a **Python automation tool** that ingests daily security metrics, calculates KPIs, detects 7-day trends, and generates a complete dashboard report — in under **3 minutes**.

## 📊 Real-World Impact

| Metric | Before | After |
|---|---|---|
| Weekly report time | **4 hours** | **< 3 minutes** |
| KPI visibility | Delayed | **Real-time** |
| Trend detection | Manual | **Automated** |
| Error rate | High | **Near zero** |

---

## 📈 KPIs Tracked

| KPI | Description |
|---|---|
| False Positive Rate | % of alerts that were non-threats |
| Mean Time To Respond (MTTR) | Average incident response time |
| Alert Resolution Rate | Incidents closed vs opened |
| SLA Status | Whether MTTR target is met |
| Patch Compliance % | Systems up to date |
| System Uptime % | Availability metric |
| Unauthorized Attempts | Potential intrusion signals |

---

## 🛠️ Tech Stack

- **Python 3.9+**  
- **JSON** — persistent key-value metric storage  
- **datetime** — time-series tracking  
- **Standard library only** — no heavy dependencies  

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/pramodj551-oss/soc-kpi-tracker
cd soc-kpi-tracker

# 2. No dependencies needed — pure Python!

# 3. Seed sample data + generate report
python kpi_tracker.py --seed

# 4. Run daily (after first seed)
python kpi_tracker.py
```

---

## 📁 Output Files

```
results/
├── kpi_report.json       ← Full KPI report with trends
└── daily_summary.txt     ← Plain text summary for email/Slack

data/
└── metrics_store.json    ← Persistent metrics database
```

---

## 📁 Project Structure

```
soc-kpi-tracker/
│
├── kpi_tracker.py        ← Main tracking & reporting script
├── README.md             ← This file
├── data/                 ← Auto-created metrics store
└── results/              ← Auto-generated reports
```

---

## 🔄 How to Feed Real Data

Replace the `generate_sample_data()` section in `log_daily_metrics()` with your actual SIEM output:

```python
# Example: replace with your SIEM CSV export
import pandas as pd
df = pd.read_csv("siem_daily_export.csv")
data = {
    "total_alerts": df["alert_count"].sum(),
    "critical_alerts": df[df["severity"]=="CRITICAL"].shape[0],
    # ... map your columns
}
```

---

## 🎓 Learning Context

Built as part of the **Applied AI & ML Essentials** program at **IIT Patna (Vishlesan i-Hub)**, solving a real operational bottleneck I experienced as a SOC Supervisor.

---

*Part of my AI Security portfolio — [pramodjadhav.vercel.app](https://pramodjadhav.vercel.app)*
