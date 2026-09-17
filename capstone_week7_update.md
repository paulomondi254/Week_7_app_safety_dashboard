# 📊 Capstone Progress Check — Week 7

**Team:** NULL_TERMINATORS (KPC Cohort, Inuka Fellowship, Power Learn Project)  
**Project:** Predictive Maintenance for KPC Pipeline Pump Infrastructure  
**Submitted By:** Brian Kioko (ML & Modelling Engineering Lead)  
**Date:** August 2026  

---

## 📈 Executive Summary

Week 7 focused primarily on establishing the core data engineering and telemetry reconciliation pipeline supporting predictive maintenance for 24 pipeline pumps across 4 operational depots. Per our Implementation Rollout Plan, frontend dashboard scaffolding commences in Phase 2, while Phase 1 (Weeks 7–12) establishes high-integrity Health Indicators (HI).

---

## 🛠️ Key Progress & Deliverables

| Module | Status | Deliverable Details |
| :--- | :--- | :--- |
| **SCADA Telemetry Alignment** | `COMPLETED` | Aligned historical SCADA metrics (suction/discharge pressure, flow rate, motor current) across 24 pumps. |
| **Flowgard Reconciliation** | `IN PROGRESS` | Computed performance residuals (`Residual = Actual Pressure - Simulated Pressure`) as primary Health Indicators. |
| **Time-Series Storage** | `COMPLETED` | Implemented Pandas HDF5 & Parquet feature stores for high-throughput time-series degradation analysis. |
| **Noise Reduction** | `IN PROGRESS` | Applied Exponentially Weighted Moving Average (EWMA) smoothing via SciPy to isolate long-term pump wear. |

---

## 💻 Tech Stack & Data Engineering Framework

* **Pandas & NumPy**: Data ingestion, normalization, and residual calculations.
* **SciPy**: Digital filtering, signal smoothing, and residual baseline estimation.
* **Scikit-Learn**: Machine learning feature extraction and composite risk score calculations.
* **Next.js & Plotly.js** *(Phase 2 Target)*: Stakeholder-facing predictive maintenance web application.

---

## ⚠️ Operational Challenge & Proposed Mitigation

> [!WARNING]
> **Challenge: Synthetic vs. Real-World SCADA Transients**  
> Synthetic datasets exhibit relatively linear degradation curves. Real-world KPC pipeline operations contain transients (product changeovers, batch switching, pump start/stop cycles) that induce transient residual spikes, risking false anomaly alarms.

### 🛡️ Mitigation Strategy: Two-Tier Data & Visualization Pipeline
1. **Raw Residual View (Technical / Engineering Tier)**: Displays unfiltered telemetry spikes alongside SCADA event logs to assist data engineers in diagnosing operational transients vs true mechanical faults.
2. **Degradation Trend View (Operations / Management Tier)**: Uses EWMA moving-window filtering to strip high-frequency operational noise, isolating structural pump degradation curves for shift operators.

---

## 🎯 Next Week Milestone (Week 8 Target)

* Complete the **Flowgard SCADA Reconciliation Pipeline** for all 24 synthetic pumps.
* Deliver a standardized, ready-to-consume feature store in CSV/Parquet format to the frontend team by the conclusion of Week 8.