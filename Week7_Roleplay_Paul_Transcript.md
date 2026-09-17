# Week 7 Role-play Video Transcript & Script
**Presenter:** Brian Kioko (HSE Lead / ML Engineering Lead)  
**Target Audience:** Depot B Operations Supervisors, Maintenance Crew, and HSE Committee  
**Topic:** HSE Safety Briefing — Slip/Trip Surge & Safety Command Center Dashboard Walkthrough  
**Video File:** `Week7_Roleplay_BrianKioko.mp4`  

---

## 🎬 Video Overview & Slide Breakdown

### Slide 1: Introduction & Executive Briefing
- **Visual:** Executive Title Card with Safety Command Center Branding.
- **Audio / Dialogue:**  
  > "Hello team. This is Brian Kioko, HSE and Safety Engineering Lead. Welcome to this Week 7 operational safety briefing. Today we are addressing a critical hazard trend flagged by our Safety Command Center dashboard. Over the past 30 days, we have observed a 40% increase in slip and trip incidents at Depot B, specifically concentrated during the Night Shift."

---

### Slide 2: Data Insights & Incident Trends (Dashboard Analytics)
- **Visual:** Metric cards (Total Incidents: 304, Critical: 84, Avg Severity: 2.3/5, Injuries: 77) + Incident Type Bar Chart.
- **Audio / Dialogue:**  
  > "Looking at our quantitative data from `app_safety_dashboard.py`, slip and trip hazards account for over a quarter of total reported events across facility sites. While many resulted in first-aid treatments, several had credible worst-case potential for life-altering injury. When we apply dynamic filters by site and shift, Depot B night operations emerge as our highest risk zone."

---

### Slide 3: Risk Heatmap & Geographical Hotspots
- **Visual:** Shift vs Weekday Heatmap & Scatter Mapbox Density Visualization.
- **Audio / Dialogue:**  
  > "Our shift-versus-weekday heatmap reveals that Mondays and Thursdays on the Night Shift experience peak incident frequency. Furthermore, our GPS spatial density map confirms that these incidents are clustered around the fluid transfer walkways and unlit loading bays at Depot B. Reduced visibility, oil residue, and fatigued footwear grip during late shifts are the primary contributing factors."

---

### Slide 4: Corrective Action Plan & Safety Alert Memo
- **Visual:** Safety Alert PDF Summary (`Week7_Safety_Alert_BrianKioko.pdf`) listing 4 Required Actions.
- **Audio / Dialogue:**  
  > "To address this immediately, we have issued the official Safety Alert memo for Depot B. We are implementing four mandatory field actions:  
  > 1. **Immediate Spill Cleanup**: Cordon off and report any liquid or oil residue on transfer walkways immediately.  
  > 2. **Pre-Shift Footwear Audits**: Inspect non-slip sole treads before starting every shift; request immediate replacement for worn tread.  
  > 3. **Walkway Lighting Repair**: Promptly report dark or flickering fixtures around loading bays to the Control Room.  
  > 4. **Stop-Work & Tag-Out**: Empower all personnel to pause tasks whenever unsafe floor conditions are identified."

---

### Slide 5: Dashboard Alert Threshold Demo & Closing
- **Visual:** Live Streamlit Sidebar Threshold Control & Alert Banners (High Alert / Watch / Success).
- **Audio / Dialogue:**  
  > "Finally, let's look at how our Safety Command Center threshold system keeps us accountable. By setting our critical alert threshold to 5 incidents, the dashboard dynamically triggers automated high-visibility warning banners as field data updates. This provides immediate operational visibility for supervisors before incidents escalate. Let's stay proactive, look out for one another, and ensure everyone goes home safe at the end of every shift. See it, report it, fix it. Thank you."

---

## 📋 Summary of Key Deliverables Addressed
- **Dashboard Code (`app_safety_dashboard.py`)**: Fully integrated dynamic filtering, metric scorecards, Plotly heatmap, mapbox density, and threshold warning alerts.
- **Safety Alert Memo (`Week7_Safety_Alert_BrianKioko.pdf`)**: Formal written bulletin distributed to field teams.
- **Role-play Video (`Week7_Roleplay_BrianKioko.mp4`)**: MP4 presentation delivering HSE communications.
- **Capstone Progress Update (`capstone_week7_update.md`)**: Detailed report on SCADA telemetry & predictive risk modeling.
