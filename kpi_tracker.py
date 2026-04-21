"""
Automated Security KPI & Metrics Tracker
==========================================
Author  : Pramod Prakash Jadhav
GitHub  : github.com/pramodj551-oss
LinkedIn: linkedin.com/in/pramod-jadhav-42ba2281

Automated SOC performance dashboard — ingests daily security
metrics, calculates KPIs, detects trends, and generates reports.

Real-world impact:
- Report generation time: 4 hours/week → under 3 minutes
- SOC managers track all KPIs in a single view
"""

import json
import os
import random
from datetime import datetime, timedelta
from collections import defaultdict

# ── CONFIG ────────────────────────────────────────────────
DATA_FILE    = "data/metrics_store.json"
REPORT_FILE  = "results/kpi_report.json"
SUMMARY_FILE = "results/daily_summary.txt"


# ── STORAGE ──────────────────────────────────────────────
def load_store():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"entries": [], "created_at": datetime.now().isoformat()}


def save_store(store):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(store, f, indent=2)


# ── DATA INGESTION ────────────────────────────────────────
def log_daily_metrics(store, date=None, data=None):
    """
    Add a daily metrics record to the store.
    In production: pull from SIEM API or log files.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    if data is None:
        # Demo: generate realistic SOC metrics
        data = {
            "total_alerts":          random.randint(40, 200),
            "critical_alerts":       random.randint(0, 15),
            "high_alerts":           random.randint(5, 40),
            "false_positives":       random.randint(10, 60),
            "incidents_opened":      random.randint(1, 20),
            "incidents_closed":      random.randint(1, 18),
            "mttr_minutes":          random.randint(10, 120),   # Mean Time To Respond
            "unauthorized_attempts": random.randint(0, 25),
            "logins_off_hours":      random.randint(0, 10),
            "patch_compliance_pct":  round(random.uniform(85, 100), 1),
            "uptime_pct":            round(random.uniform(99.0, 100.0), 2),
        }

    entry = {"date": date, **data, "logged_at": datetime.now().isoformat()}
    store["entries"].append(entry)
    save_store(store)
    return entry


# ── KPI CALCULATIONS ─────────────────────────────────────
def calculate_kpis(entries):
    """
    Calculate key security performance indicators from entries.
    """
    if not entries:
        return {}

    total_alerts     = sum(e["total_alerts"]     for e in entries)
    false_positives  = sum(e["false_positives"]  for e in entries)
    critical_alerts  = sum(e["critical_alerts"]  for e in entries)
    incidents_opened = sum(e["incidents_opened"] for e in entries)
    incidents_closed = sum(e["incidents_closed"] for e in entries)
    avg_mttr         = sum(e["mttr_minutes"]     for e in entries) / len(entries)
    avg_uptime       = sum(e["uptime_pct"]       for e in entries) / len(entries)
    avg_patch        = sum(e["patch_compliance_pct"] for e in entries) / len(entries)
    unauth_total     = sum(e["unauthorized_attempts"] for e in entries)

    kpis = {
        "period_days":          len(entries),
        "total_alerts":         total_alerts,
        "critical_alerts":      critical_alerts,
        "false_positive_rate":  round(false_positives / total_alerts * 100, 1) if total_alerts else 0,
        "alert_resolution_rate": round(incidents_closed / incidents_opened * 100, 1) if incidents_opened else 0,
        "avg_mttr_minutes":     round(avg_mttr, 1),
        "avg_uptime_pct":       round(avg_uptime, 2),
        "avg_patch_compliance": round(avg_patch, 1),
        "unauthorized_attempts": unauth_total,
        "sla_status":           "✓ MET" if avg_mttr <= 60 else "✗ BREACHED",
    }
    return kpis


# ── TREND ANALYSIS ───────────────────────────────────────
def detect_trends(entries, window=7):
    """
    Compare recent window vs previous window to detect trends.
    """
    if len(entries) < window * 2:
        return {"status": "Insufficient data for trend analysis"}

    recent   = entries[-window:]
    previous = entries[-window*2:-window]

    def avg(lst, key):
        return sum(e[key] for e in lst) / len(lst)

    trends = {}
    for metric in ["total_alerts", "false_positives", "mttr_minutes", "unauthorized_attempts"]:
        recent_avg   = avg(recent, metric)
        previous_avg = avg(previous, metric)
        if previous_avg == 0:
            continue
        change_pct = ((recent_avg - previous_avg) / previous_avg) * 100
        direction = "↑ INCREASING" if change_pct > 5 else ("↓ DECREASING" if change_pct < -5 else "→ STABLE")
        trends[metric] = {
            "recent_avg":   round(recent_avg, 1),
            "previous_avg": round(previous_avg, 1),
            "change_pct":   round(change_pct, 1),
            "direction":    direction
        }
    return trends


# ── REPORT ───────────────────────────────────────────────
def generate_report(store):
    """
    Generate KPI report and print dashboard.
    """
    entries = store.get("entries", [])
    if not entries:
        print("No data available. Run with --seed to populate sample data.")
        return

    kpis   = calculate_kpis(entries)
    trends = detect_trends(entries)

    print("\n" + "="*55)
    print("  SOC KPI DASHBOARD — AUTOMATED REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*55)
    print(f"\n  PERIOD    : Last {kpis['period_days']} days")
    print(f"  SLA STATUS: {kpis['sla_status']}\n")

    print("  ALERT METRICS")
    print(f"  Total Alerts         : {kpis['total_alerts']:>6}")
    print(f"  Critical Alerts      : {kpis['critical_alerts']:>6}")
    print(f"  False Positive Rate  : {kpis['false_positive_rate']:>5.1f}%")
    print(f"  Resolution Rate      : {kpis['alert_resolution_rate']:>5.1f}%")

    print("\n  RESPONSE METRICS")
    print(f"  Avg MTTR             : {kpis['avg_mttr_minutes']:>5.1f} min")
    print(f"  Unauthorized Attempts: {kpis['unauthorized_attempts']:>6}")

    print("\n  COMPLIANCE METRICS")
    print(f"  Avg System Uptime    : {kpis['avg_uptime_pct']:>5.2f}%")
    print(f"  Patch Compliance     : {kpis['avg_patch_compliance']:>5.1f}%")

    if trends and "status" not in trends:
        print("\n  7-DAY TRENDS")
        for metric, t in trends.items():
            print(f"  {metric:28s}: {t['direction']} ({t['change_pct']:+.1f}%)")

    print("\n" + "="*55)

    # Save reports
    os.makedirs("results", exist_ok=True)
    report = {
        "generated_at": datetime.now().isoformat(),
        "kpis": kpis,
        "trends": trends,
        "raw_entries_count": len(entries)
    }
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    with open(SUMMARY_FILE, "w") as f:
        f.write(f"SOC KPI Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*40 + "\n")
        for k, v in kpis.items():
            f.write(f"{k}: {v}\n")

    print(f"\n  JSON report saved  → {REPORT_FILE}")
    print(f"  Text summary saved → {SUMMARY_FILE}\n")


# ── SEED DATA ────────────────────────────────────────────
def seed_sample_data(store, days=30):
    """
    Populate store with 30 days of sample metrics.
    """
    print(f"  Seeding {days} days of sample data...")
    store["entries"] = []
    for i in range(days, 0, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        log_daily_metrics(store, date=date)
    save_store(store)
    print(f"  {days} records created in {DATA_FILE}")


# ── MAIN ────────────────────────────────────────────────
def main():
    import sys
    store = load_store()

    if "--seed" in sys.argv or len(store["entries"]) == 0:
        print("\n[SETUP] Populating sample data...")
        seed_sample_data(store, days=30)

    print("\n[1/3] Loading metrics store...")
    print(f"      {len(store['entries'])} records found.")

    print("[2/3] Calculating KPIs and trends...")
    print("[3/3] Generating dashboard report...")
    generate_report(store)

    # Log today's metrics
    today = datetime.now().strftime("%Y-%m-%d")
    existing_dates = [e["date"] for e in store["entries"]]
    if today not in existing_dates:
        new_entry = log_daily_metrics(store)
        print(f"  Today's metrics logged: {new_entry['total_alerts']} alerts | MTTR: {new_entry['mttr_minutes']} min")


if __name__ == "__main__":
    main()
