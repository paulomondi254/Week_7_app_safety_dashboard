import os
import wave
import math
import struct
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH, HEIGHT = 1920, 1080
SLIDE_DURATION = 5.0  # seconds per slide
NUM_SLIDES = 5
TOTAL_DURATION = SLIDE_DURATION * NUM_SLIDES

os.makedirs('slides_temp', exist_ok=True)

# Helper for drawing rounded rectangles
def draw_card(draw, box, fill, outline=None, width=1, radius=15):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# Helper for text headers & body
def create_slide_base():
    img = Image.new('RGB', (WIDTH, HEIGHT), color='#0F172A')
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw_card(draw, (40, 40, WIDTH - 40, 140), fill='#1E293B', outline='#334155', width=2)
    draw.text((70, 60), "🛡️ SAFETY COMMAND CENTER", fill='#38BDF8', font_size=40)
    draw.text((WIDTH - 450, 70), "WEEK 7 ROLE-PLAY PRESENTATION", fill='#94A3B8', font_size=22)
    
    # Footer bar
    draw_card(draw, (40, HEIGHT - 80, WIDTH - 40, HEIGHT - 30), fill='#1E293B', outline='#334155', width=1)
    draw.text((70, HEIGHT - 65), "Presenter: Brian Kioko (HSE & ML Lead)", fill='#CBD5E1', font_size=20)
    draw.text((WIDTH - 420, HEIGHT - 65), "File: Week7_Roleplay_BrianKioko.mp4", fill='#38BDF8', font_size=20)
    
    return img, draw

# ---------- SLIDE 1: TITLE CARD ----------
def make_slide1():
    img, draw = create_slide_base()
    
    # Main hero box
    draw_card(draw, (200, 220, WIDTH - 200, 850), fill='#1E293B', outline='#0284C7', width=3, radius=25)
    
    draw.text((260, 280), "🚨 EXECUTIVE SAFETY BRIEFING", fill='#EF4444', font_size=32)
    draw.text((260, 350), "Addressing Depot B Night Shift Incident Surge", fill='#F8FAFC', font_size=52)
    draw.text((260, 440), "Insights & Field Action Plan from Safety Command Center Data", fill='#94A3B8', font_size=28)
    
    # Key details box
    draw_card(draw, (260, 520, WIDTH - 260, 780), fill='#0F172A', outline='#334155', width=2, radius=15)
    draw.text((300, 550), "📍 Primary Location: Depot B (Night Shift Operations)", fill='#E2E8F0', font_size=26)
    draw.text((300, 600), "⚠️ Identified Hazard: 40% Increase in Slip, Trip & Fall Incidents", fill='#F59E0B', font_size=26)
    draw.text((300, 650), "📊 Target Audience: Operations Supervisors, HSE Committee & Maintenance Crew", fill='#E2E8F0', font_size=26)
    draw.text((300, 700), "🎯 Objective: Data Transparency, Alert Thresholding & Immediate Risk Mitigation", fill='#38BDF8', font_size=26)
    
    img.save('slides_temp/slide1.png')

# ---------- SLIDE 2: KPI & INCIDENT BREAKDOWN ----------
def make_slide2():
    img, draw = create_slide_base()
    
    draw.text((70, 160), "📊 Quantitative Dashboard Analytics", fill='#F8FAFC', font_size=38)
    
    # 4 Metric Cards
    metrics = [
        ("TOTAL INCIDENTS", "304", "#38BDF8", (70, 230, 480, 390)),
        ("CRITICAL (SEV 4+)", "84", "#EF4444", (520, 230, 930, 390)),
        ("AVG SEVERITY", "2.30 / 5.0", "#F59E0B", (970, 230, 1380, 390)),
        ("TOTAL INJURIES", "77", "#10B981", (1420, 230, 1850, 390)),
    ]
    for label, val, color, box in metrics:
        draw_card(draw, box, fill='#1E293B', outline=color, width=2)
        draw.text((box[0] + 30, box[1] + 25), label, fill='#94A3B8', font_size=20)
        draw.text((box[0] + 30, box[1] + 65), val, fill=color, font_size=42)
        
    # Main chart & callout
    draw_card(draw, (70, 430, 1100, 950), fill='#1E293B', outline='#334155', width=2)
    draw.text((100, 460), "Incident Type Distribution (app_safety_dashboard.py)", fill='#F8FAFC', font_size=28)
    
    categories = [
        ("Slip / Trip / Fall", 28, "#EF4444"),
        ("Equipment Contact", 22, "#F59E0B"),
        ("Vehicle Interaction", 18, "#38BDF8"),
        ("Chemical Exposure", 15, "#10B981"),
        ("Manual Handling", 12, "#8B5CF6"),
        ("Fall From Height", 5, "#EC4899"),
    ]
    y_offset = 530
    for name, pct, col in categories:
        draw.text((100, y_offset), name, fill='#E2E8F0', font_size=22)
        # Bar background
        draw_card(draw, (380, y_offset + 5, 950, y_offset + 25), fill='#0F172A')
        # Filled bar
        bar_w = int(380 + (950 - 380) * (pct / 30.0))
        draw_card(draw, (380, y_offset + 5, bar_w, y_offset + 25), fill=col)
        draw.text((970, y_offset), f"{pct}%", fill=col, font_size=22)
        y_offset += 65
        
    # Callout panel
    draw_card(draw, (1140, 430, 1850, 950), fill='#1E293B', outline='#EF4444', width=3)
    draw.text((1170, 470), "🚨 Critical Finding", fill='#EF4444', font_size=30)
    draw.text((1170, 540), "Slip and trip hazards represent", fill='#F8FAFC', font_size=26)
    draw.text((1170, 580), "the single largest incident category,", fill='#F8FAFC', font_size=26)
    draw.text((1170, 620), "with Depot B Night Shift showing a", fill='#F8FAFC', font_size=26)
    draw.text((1170, 660), "40% statistically significant surge.", fill='#F59E0B', font_size=26)
    
    draw_card(draw, (1170, 730, 1820, 900), fill='#0F172A', outline='#334155', width=1)
    draw.text((1190, 755), "• Credible worst-case: Life-altering harm", fill='#94A3B8', font_size=20)
    draw.text((1190, 800), "• High occurrence: Mondays & Thursdays", fill='#94A3B8', font_size=20)
    draw.text((1190, 845), "• Root cause: Reduced visibility & leaks", fill='#94A3B8', font_size=20)

    img.save('slides_temp/slide2.png')

# ---------- SLIDE 3: RISK HEATMAP & MAP ----------
def make_slide3():
    img, draw = create_slide_base()
    
    draw.text((70, 160), "🗺️ Heatmap & Spatial Hotspot Identification", fill='#F8FAFC', font_size=38)
    
    # Heatmap box
    draw_card(draw, (70, 230, 930, 950), fill='#1E293B', outline='#334155', width=2)
    draw.text((100, 260), "Shift vs. Weekday Incident Heatmap", fill='#F8FAFC', font_size=28)
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    shifts = ['Day Shift', 'Swing Shift', 'Night Shift']
    
    # Draw grid table
    for j, day in enumerate(days):
        draw.text((320 + j * 85, 330), day, fill='#94A3B8', font_size=20)
        
    matrix_data = [
        [12, 8, 10, 14, 15, 6, 4],   # Day
        [9,  7, 11, 10, 12, 5, 3],   # Swing
        [28, 14, 16, 32, 22, 12, 8]   # Night
    ]
    
    for i, shift in enumerate(shifts):
        draw.text((100, 380 + i * 160), shift, fill='#E2E8F0', font_size=22)
        for j, val in enumerate(matrix_data[i]):
            # Color intensity
            intensity = min(255, val * 7)
            fill_col = f"#{intensity:02x}2020" if val > 20 else ("#503010" if val > 10 else "#102030")
            text_col = "#FFFFFF" if val > 20 else "#CBD5E1"
            box_coords = (300 + j * 85, 360 + i * 160, 375 + j * 85, 480 + i * 160)
            draw_card(draw, box_coords, fill=fill_col, outline='#334155', width=1)
            draw.text((325 + j * 85, 405 + i * 160), str(val), fill=text_col, font_size=26)
            
    # Location GPS Density box
    draw_card(draw, (970, 230, 1850, 950), fill='#1E293B', outline='#38BDF8', width=2)
    draw.text((1000, 260), "📍 GPS Density Map Hotspot Analysis", fill='#38BDF8', font_size=28)
    
    draw_card(draw, (1000, 320, 1820, 650), fill='#0F172A', outline='#334155', width=1)
    draw.text((1040, 360), "HOTSPOT CLUSTER: Depot B (Lat: 41.8781, Lon: -87.6298)", fill='#EF4444', font_size=24)
    draw.text((1040, 420), "• Walkway Segment B-4 (Fluid Transfer Manifold)", fill='#E2E8F0', font_size=22)
    draw.text((1040, 470), "• Loading Bay 2 Walkway (Low Light Fixture #14)", fill='#E2E8F0', font_size=22)
    draw.text((1040, 520), "• Pump House Access Ramp (Oil Accumulation Zone)", fill='#E2E8F0', font_size=22)
    draw.text((1040, 580), "Status: Immediate HSE Field Audit Required", fill='#F59E0B', font_size=22)
    
    # Key takeaways
    draw_card(draw, (1000, 680, 1820, 920), fill='#0F172A', outline='#10B981', width=2)
    draw.text((1030, 710), "✅ Target Interventions", fill='#10B981', font_size=26)
    draw.text((1030, 760), "1. Focus resources on Night Shift Monday/Thursday routines", fill='#CBD5E1', font_size=20)
    draw.text((1030, 805), "2. Install anti-slip grating on Transfer Manifold Walkway B-4", fill='#CBD5E1', font_size=20)
    draw.text((1030, 850), "3. Replace lighting ballast at Loading Bay 2", fill='#CBD5E1', font_size=20)

    img.save('slides_temp/slide3.png')

# ---------- SLIDE 4: SAFETY ALERT MEMO ----------
def make_slide4():
    img, draw = create_slide_base()
    
    draw.text((70, 160), "🚨 Written Safety Alert Bulletin (Week7_Safety_Alert_BrianKioko.pdf)", fill='#F8FAFC', font_size=38)
    
    # Outer memo box
    draw_card(draw, (70, 230, 1850, 950), fill='#1E293B', outline='#EF4444', width=3)
    
    # Banner
    draw_card(draw, (100, 260, 1820, 350), fill='#7F1D1D', outline='#EF4444', width=2)
    draw.text((140, 285), "SAFETY ALERT: PREVENTING SLIPS & TRIPS AT DEPOT B", fill='#F8FAFC', font_size=36)
    
    # 4 Action items grid
    actions = [
        ("🧹 Clean Up Spills Immediately", "Do not walk past liquid, oil, or debris. Cordon off larger spills and notify Maintenance.", (100, 380, 940, 620)),
        ("👷 Check Safety Footwear", "Inspect non-slip footwear tread before every shift. Request immediate replacement for worn soles.", (980, 380, 1820, 620)),
        ("💡 Report Poor Lighting", "Report flickering or failed lights around walkways and loading bays to Control Room immediately.", (100, 650, 940, 890)),
        ("⚠️ Take Ownership & Stop Work", "Empower all workers to stop unsafe tasks, tag hazards, and maintain a zero-harm environment.", (980, 650, 1820, 890)),
    ]
    
    for title, desc, box in actions:
        draw_card(draw, box, fill='#0F172A', outline='#334155', width=2)
        draw.text((box[0] + 30, box[1] + 30), title, fill='#38BDF8', font_size=26)
        
        # Word wrap text manually
        words = desc.split()
        lines, line = [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 42:
                lines.append(" ".join(line[:-1]))
                line = [w]
        if line:
            lines.append(" ".join(line))
            
        for k, l_text in enumerate(lines):
            draw.text((box[0] + 30, box[1] + 85 + k * 32), l_text, fill='#CBD5E1', font_size=20)
            
    img.save('slides_temp/slide4.png')

# ---------- SLIDE 5: THRESHOLD ALERT DEMO & CONCLUSION ----------
def make_slide5():
    img, draw = create_slide_base()
    
    draw.text((70, 160), "⚙️ Dashboard Alert Thresholds & Executive Conclusion", fill='#F8FAFC', font_size=38)
    
    # Left box: Streamlit sidebar alert system
    draw_card(draw, (70, 230, 930, 950), fill='#1E293B', outline='#38BDF8', width=2)
    draw.text((100, 260), "Sidebar Critical Threshold System", fill='#38BDF8', font_size=28)
    
    draw_card(draw, (100, 320, 900, 420), fill='#0F172A', outline='#334155', width=1)
    draw.text((130, 350), "🚨 Threshold Setting: 5 Critical Incidents", fill='#F59E0B', font_size=24)
    
    # Alert states
    draw_card(draw, (100, 450, 900, 580), fill='#7F1D1D', outline='#EF4444', width=2)
    draw.text((130, 480), "⚠️ HIGH ALERT (Active)", fill='#FFFFFF', font_size=26)
    draw.text((130, 525), "Triggered when Critical Incidents >= Threshold (Current: 84 >= 5)", fill='#FCA5A5', font_size=18)
    
    draw_card(draw, (100, 610, 900, 720), fill='#1E3A8A', outline='#3B82F6', width=1)
    draw.text((130, 640), "ℹ️ WATCH ALERT (60% - 99% Threshold)", fill='#FFFFFF', font_size=22)
    draw.text((130, 680), "Monitors near-miss buildup prior to critical breach.", fill='#93C5FD', font_size=18)
    
    draw_card(draw, (100, 750, 900, 860), fill='#064E3B', outline='#10B981', width=1)
    draw.text((130, 780), "✅ NORMAL OPERATIONAL STATUS", fill='#FFFFFF', font_size=22)
    draw.text((130, 820), "Target steady state for all facility sites.", fill='#A7F3D0', font_size=18)

    # Right box: Closing commitment
    draw_card(draw, (970, 230, 1850, 950), fill='#1E293B', outline='#10B981', width=3)
    draw.text((1000, 280), "🛡️ HSE Commitment & Next Steps", fill='#10B981', font_size=32)
    
    draw.text((1000, 360), "1. Deploy app_safety_dashboard.py to site supervisors", fill='#F8FAFC', font_size=24)
    draw.text((1000, 430), "2. Conduct mandatory pre-shift safety stand-downs", fill='#F8FAFC', font_size=24)
    draw.text((1000, 500), "3. Execute Depot B footwear and lighting audit", fill='#F8FAFC', font_size=24)
    draw.text((1000, 570), "4. Review weekly KPI progress on Monday morning", fill='#F8FAFC', font_size=24)
    
    draw_card(draw, (1000, 670, 1820, 900), fill='#0F172A', outline='#F59E0B', width=2)
    draw.text((1150, 730), "SEE IT. REPORT IT. FIX IT.", fill='#F59E0B', font_size=38)
    draw.text((1100, 810), "Every hazard corrected ensures everyone goes home safe.", fill='#CBD5E1', font_size=22)

    img.save('slides_temp/slide5.png')

print("Generating slides...")
make_slide1()
make_slide2()
make_slide3()
make_slide4()
make_slide5()
print("All 5 presentation slides generated successfully!")

# ---------- AUDIO GENERATION (SYNTHESIZED HARMONIC TRACK) ----------
print("Synthesizing audio track...")
sample_rate = 44100
n_samples = int(sample_rate * TOTAL_DURATION)

with wave.open('roleplay_audio.wav', 'w') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)
    
    for i in range(n_samples):
        t = i / sample_rate
        # Background ambient tone
        freq = 220 + 4 * math.sin(2 * math.pi * 0.2 * t)
        val = int(3500 * math.sin(2 * math.pi * freq * t))
        
        # Add slide transition chimes at t=5.0, 10.0, 15.0, 20.0
        for transition_t in [5.0, 10.0, 15.0, 20.0]:
            if transition_t <= t <= transition_t + 0.3:
                chime_t = t - transition_t
                chime_val = int(8000 * math.sin(2 * math.pi * 880 * chime_t) * math.exp(-10 * chime_t))
                val += chime_val
                
        val = max(-32768, min(32767, val))
        wav.writeframes(struct.pack('<h', val))

print("Audio track roleplay_audio.wav generated!")

# ---------- FFMPEG MP4 VIDEO ENCODING ----------
print("Encoding Week7_Roleplay_BrianKioko.mp4 with ffmpeg...")
cmd = [
    'ffmpeg', '-y',
    '-loop', '1', '-t', '5', '-i', 'slides_temp/slide1.png',
    '-loop', '1', '-t', '5', '-i', 'slides_temp/slide2.png',
    '-loop', '1', '-t', '5', '-i', 'slides_temp/slide3.png',
    '-loop', '1', '-t', '5', '-i', 'slides_temp/slide4.png',
    '-loop', '1', '-t', '5', '-i', 'slides_temp/slide5.png',
    '-i', 'roleplay_audio.wav',
    '-filter_complex',
    '[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0[v]',
    '-map', '[v]', '-map', '5:a',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '24',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    'Week7_Roleplay_BrianKioko.mp4'
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: Week7_Roleplay_BrianKioko.mp4 created successfully!")
else:
    print("FFMPEG Error:", res.stderr)
