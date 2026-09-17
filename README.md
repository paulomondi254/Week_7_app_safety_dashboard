**🛡️ Safety Command Center — Week 7 Complete Submission**  
An interactive **HSE Safety Analytics Dashboard & Emergency Command Center** built with  **Streamlit, Pandas, and Plotly**, paired with mandatory Health, Safety, and Environment (HSE) field communication deliverables.  
![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OMQ2AABAAsSPBCj7fFwtCmJHAjAU2QtIq6DIzW7UHAMBfnGt1V8fHEQAA3rsexOkF3va0dq8AAAAASUVORK5CYII=)  
**📁 Repository Structure & Required Deliverables**  
| | | |  
|-|-|-|  
| **Deliverable File** | **Type** | **Description** |   
| 🐍 [app_safety_dashboard.py](file:///home/tristan/Documents/Repos/wk7/app_safety_dashboard.py "file:///home/tristan/Documents/Repos/wk7/app_safety_dashboard.py") | **Python Application** | Full Streamlit dashboard featuring smart column detection, dynamic filters, metric scorecards, alert thresholds, 5 Plotly charts, and CSV data export. |   
| 📄 [Week7_Safety_Alert_BrianKioko.pdf](file:///home/tristan/Documents/Repos/wk7/Week7_Safety_Alert_BrianKioko.pdf "file:///home/tristan/Documents/Repos/wk7/Week7_Safety_Alert_BrianKioko.pdf") | **Written Safety Alert** | Official HSE field safety bulletin detailing immediate corrective actions for Depot B night shift slip/trip surge. |   
| 🎬 [Week7_Roleplay_BrianKioko.mp4](file:///home/tristan/Documents/Repos/wk7/Week7_Roleplay_BrianKioko.mp4 "file:///home/tristan/Documents/Repos/wk7/Week7_Roleplay_BrianKioko.mp4") | **Recorded Role-Play Video** | 1080p recorded safety briefing video delivering HSE findings, dashboard threshold walkthrough, and corrective action plan. |   
| 📝 [Week7_Roleplay_BrianKioko_Transcript.md](file:///home/tristan/Documents/Repos/wk7/Week7_Roleplay_BrianKioko_Transcript.md "file:///home/tristan/Documents/Repos/wk7/Week7_Roleplay_BrianKioko_Transcript.md") | **Role-Play Script** | Written transcript and slide breakdown for the recorded role-play presentation. |   
| 📊 [capstone_week7_update.md](file:///home/tristan/Documents/Repos/wk7/capstone_week7_update.md "file:///home/tristan/Documents/Repos/wk7/capstone_week7_update.md") | **Capstone Update** | Week 7 progress report on KPC Pipeline Pump Infrastructure predictive maintenance & Flowgard SCADA telemetry reconciliation. |   
| 📋 [data/safety_incidents.csv](file:///home/tristan/Documents/Repos/wk7/data/safety_incidents.csv "file:///home/tristan/Documents/Repos/wk7/data/safety_incidents.csv") | **Dataset** | HSE safety incident records with automated site mapping, shift tagging, severity scores, and spatial coordinates. |   
   
![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANElEQVR4nO3OQQmAUBBAwSfIb+HdmNvAkgaxgjcRZhLMNjNHdQUAwF/ce7Wq8+sJAACvrQctewNKtdojwQAAAABJRU5ErkJggg==)  
**🚀 Key Dashboard Features (**app_safety_dashboard.py **)**  
- **Smart Delimiter & Column Detection**: Auto-detects dates, shift names, site aliases, incident categories, and spatial coordinates.  
- **Dynamic Multi-Field Filters**: Interactive filtering by site, custom date range, incident category, and operational shift.  
- **Metric Scorecards**: Real-time KPI counters for Total Incidents, Critical Incidents (Sev 4+), Average Severity, and Total Injuries.  
- **Threshold Warning Systems**: Configurable critical incident alert banner (triggers High Alert, Watch, or Normal status banners).  
- **Interactive Analytics**:  
  - Incident Trend Line & Bar Chart  
  - Incident Breakdown by Category  
  - Shift vs. Weekday Incident Density Heatmap  
  - Incidents by Site Distribution  
  - Geographic Hotspot Density Map (Scatter Mapbox)  
- **Filtered Data Export**: Download raw or filtered HSE data as CSV for auditing.  
![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANklEQVR4nO3OQQmAABRAsSeYxZw/lieLGMACBrCCNxG2BFtmZquOAAD4i3Ot7mr/egIAwGvXA6fGBdgoVMwYAAAAAElFTkSuQmCC)  
**🛠️ Quickstart Guide**  
**1. Clone & Activate Environment**  
git clone git@github.com:paulomondi254/Safety-Command.git  
 cd Safety-Command  
   
 # Create virtual environment  
 python3 -m venv venv  
 source venv/bin/activate  
   
 # Install dependencies  
 pip install -r requirements.txt  
   
**2. Run the Safety Dashboard**  
streamlit run app_safety_dashboard.py  
   
Access the application at: http://localhost:8501  
![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANElEQVR4nO3OUQmAABBAsSeILQSjXgcrmkOs4J8IW4ItM7NXZwAA/MW1Vlt1fBwBAOC9+wEukwQ+V/SggAAAAABJRU5ErkJggg==)  
**📸 Visual Overview**  
   
   
![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnEAAAACCAYAAAA3pIp+AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAANUlEQVR4nO3OMQ2AABAAsSNhwgJuUPYDMpnRgQU2QtIq6DIze3UGAMBf3Gu1VcfXEwAAXrseaHEEM+cJoFcAAAAASUVORK5CYII=)  
**📄 License**  
MIT License.  
