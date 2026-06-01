"""
Automated Security KPI & Metrics Tracker — Streamlit App
Author  : Pramod Prakash Jadhav
GitHub  : github.com/pramodj551-oss
LinkedIn: linkedin.com/in/pramod-jadhav-42ba2281
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from kpi_tracker import load_store, seed_sample_data, log_daily_metrics, \
                        calculate_kpis, detect_trends

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title = "SOC KPI Dashboard",
    page_icon  = "🛡️",
    layout     = "wide"
)

st.title("🛡️ Automated Security KPI & Metrics Tracker")
st.caption("Pramod Prakash Jadhav · SOC Automation · IIT Patna Applied AI & ML")

# ── LOAD / SEED DATA ──────────────────────────────────────
store = load_store()
if len(store["entries"]) == 0:
    with st.spinner("Seeding 30 days of sample data..."):
        seed_sample_data(store, days=30)
    st.success("Sample data loaded.")

entries = store["entries"]
df      = pd.DataFrame(entries)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Re-seed 30 Days of Data"):
        seed_sample_data(store, days=30)
        st.rerun()

    if st.button("➕ Log Today's Metrics"):
        from datetime import datetime
        today          = datetime.now().strftime("%Y-%m-%d")
        existing_dates = [e["date"] for e in store["entries"]]
        if today not in existing_dates:
            entry = log_daily_metrics(store)
            st.success(f"Logged: {entry['total_alerts']} alerts | MTTR: {entry['mttr_minutes']} min")
            st.rerun()
        else:
            st.info("Today's metrics already logged.")

    st.markdown("---")
    st.markdown("**About**")
    st.markdown("Reduces SOC report time from **4 hrs/week → 3 min**")

# ── KPIs ─────────────────────────────────────────────────
kpis   = calculate_kpis(entries)
trends = detect_trends(entries)

st.subheader("📊 KPI Summary")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Alerts",        kpis["total_alerts"])
c2.metric("Critical Alerts",     kpis["critical_alerts"])
c3.metric("False Positive Rate", f"{kpis['false_positive_rate']}%")
c4.metric("Avg MTTR",            f"{kpis['avg_mttr_minutes']} min")
c5.metric("SLA Status",          kpis["sla_status"])

c6, c7, c8 = st.columns(3)
c6.metric("Resolution Rate",    f"{kpis['alert_resolution_rate']}%")
c7.metric("Patch Compliance",   f"{kpis['avg_patch_compliance']}%")
c8.metric("Avg Uptime",         f"{kpis['avg_uptime_pct']}%")

st.markdown("---")

# ── CHARTS ───────────────────────────────────────────────
st.subheader("📈 Alert Trends (Last 30 Days)")

col_l, col_r = st.columns(2)

with col_l:
    fig1 = px.line(
        df, x="date",
        y=["total_alerts", "critical_alerts", "false_positives"],
        title="Daily Alert Volume",
        labels={"value": "Count", "variable": "Type"},
        color_discrete_map={
            "total_alerts":    "#4C9BE8",
            "critical_alerts": "#E84C4C",
            "false_positives": "#E8A84C",
        }
    )
    fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with col_r:
    fig2 = px.line(
        df, x="date", y="mttr_minutes",
        title="Mean Time To Respond (MTTR)",
        labels={"mttr_minutes": "Minutes"},
        color_discrete_sequence=["#4CE8A8"]
    )
    fig2.add_hline(y=60, line_dash="dash", line_color="red",
                   annotation_text="SLA Threshold (60 min)")
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

col_l2, col_r2 = st.columns(2)

with col_l2:
    fig3 = px.bar(
        df, x="date",
        y=["incidents_opened", "incidents_closed"],
        title="Incidents Opened vs Closed",
        barmode="group",
        color_discrete_map={
            "incidents_opened": "#E84C4C",
            "incidents_closed": "#4CE8A8",
        }
    )
    fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with col_r2:
    fig4 = px.line(
        df, x="date",
        y=["patch_compliance_pct", "uptime_pct"],
        title="Compliance & Uptime (%)",
        labels={"value": "%", "variable": "Metric"},
        color_discrete_map={
            "patch_compliance_pct": "#A84CE8",
            "uptime_pct":           "#4C9BE8",
        }
    )
    fig4.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

# ── TREND ANALYSIS ────────────────────────────────────────
st.markdown("---")
st.subheader("📉 7-Day Trend Analysis")

if "status" in trends:
    st.info(trends["status"])
else:
    t_cols = st.columns(len(trends))
    for col, (metric, t) in zip(t_cols, trends.items()):
        arrow = "🔴 ↑" if "INCREASING" in t["direction"] else ("🟢 ↓" if "DECREASING" in t["direction"] else "🟡 →")
        col.metric(
            label = metric.replace("_", " ").title(),
            value = t["recent_avg"],
            delta = f"{t['change_pct']:+.1f}%"
        )

# ── RAW DATA ──────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 Raw Daily Metrics Table"):
    st.dataframe(df.sort_values("date", ascending=False).reset_index(drop=True),
                 use_container_width=True)
