# app.py — COMPLETE PLATE RATIO SYSTEM (V27 ONLY SPECIAL EDITION)
# Design by Ovi • Max Plates Enforced & Excel Row Skip Fixed

import os
import copy
import random
import math
import string
from collections import Counter
from math import ceil, floor
from datetime import datetime
from io import BytesIO

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import streamlit as st
import pandas as pd

# ================================================================
# LIBRARY IMPORTS & CHECKS
# ================================================================

# Try to import reportlab for PDF
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ================================================================
# STREAMLIT PAGE CONFIGURATION
# ================================================================
st.set_page_config(
    page_title="Plate Ratio System - V27 Edition",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================================================
# MODERN CSS FOR MAIN APP
# ================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { 
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p { color: rgba(255,255,255,0.7); margin-top: 0.5rem; }
    .designer-name {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    .card:hover { border-color: rgba(102,126,234,0.5); box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 2px solid #667eea;
        display: inline-block;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        color: white;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label { font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem; }
    .best-algo {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        border-radius: 20px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        border: none;
        box-shadow: 0 10px 30px rgba(0,176,155,0.3);
        margin-bottom: 2rem;
    }
    .best-algo .metric-value { -webkit-text-fill-color: white; font-size: 1.5rem; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 12px;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102,126,234,0.4); }
    .stNumberInput input, .stTextInput input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 5px !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
    }
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.2) !important;
        background: rgba(255,255,255,0.12) !important;
    }
    .stDataFrame { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 0.5rem; }
    .warning { background: rgba(255,193,7,0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #ffc107; color: #ffc107; margin: 1rem 0; }
    .info { background: rgba(23,162,184,0.1); padding: 12px; border-radius: 12px; border-left: 4px solid #17a2b8; color: #17a2b8; }
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================================================================
# HEADER
# ================================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Plate Ratio Intelligence System</h1>
    <p>Complete Edition • Algorithm V27 Optimization • Production Ready</p>
    <p style="font-size: 0.85rem; opacity: 0.6;">AI-Powered • Fast • Accurate</p>
    <div class="designer-name">✨ Design by Ovi ✨</div>
</div>
""", unsafe_allow_html=True)


def plate_name(n: int) -> str:
    """Convert number to Excel-style column name (A, B, C, ..., Z, AA, AB, ...)"""
    n -= 1
    chars = string.ascii_uppercase
    out = ""
    while True:
        out = chars[n % 26] + out
        n = n // 26 - 1
        if n < 0:
            break
    return out


def calculate_waste_percent(plates: list, demand: dict) -> float:
    """Calculate waste percentage from plates and demand"""
    total_produced = 0
    total_demand = sum(demand.values())
    
    if total_demand == 0:
        return 0.0

    for tag in demand:
        produced_qty = 0
        for p in plates:
            if p and "layout" in p:
                ups = p["layout"].get(tag, 0)
                produced_qty += ups * p.get("sheets", 0)
        total_produced += produced_qty

    if total_produced == 0:
        return 100.0

    waste = total_produced - total_demand
    waste_percent = (waste / total_produced) * 100
    
    if waste_percent < 0:
        waste_percent = 0.0
    
    return round(waste_percent, 2)


def ensure_demand_met(plates: list, demand: dict) -> list:
    """Ensure all demand is met - no negative excess"""
    if not plates:
        return plates
    
    for tag in demand.keys():
        total_produced = 0
        for plate in plates:
            total_produced += plate["layout"].get(tag, 0) * plate["sheets"]
        
        if total_produced < demand.get(tag, 0):
            shortfall = demand.get(tag, 0) - total_produced
            if plates:
                last_plate = plates[-1]
                ups = last_plate["layout"].get(tag, 1)
                additional_sheets = ceil(shortfall / max(1, ups))
                last_plate["sheets"] += additional_sheets
    
    # Recalculate production dictionaries after sheet adjustment
    for p in plates:
        p["production"] = {tag: ups * p["sheets"] for tag, ups in p["layout"].items()}
        if "name" not in p:
            p["name"] = plate_name(p["plate_index"])
    
    return plates


def build_full_summary(plates: list, demand: dict, original_qty: dict) -> pd.DataFrame:
    """Build complete summary DataFrame"""
    rows = []
    sl = 1

    for tag in demand.keys():
        row = {
            "SL": sl,
            "Tag": tag,
            "Original QTY": original_qty.get(tag, 0),
            "Produced (+Add-on)": demand[tag]
        }

        for idx, p in enumerate(plates):
            if p and "layout" in p and "name" in p:
                ups = p["layout"].get(tag, 0)
                row[f"Plate {p['name']}"] = ups
            else:
                row[f"Plate {idx+1}"] = 0

        total_produced = 0
        for p in plates:
            if p and "layout" in p:
                ups = p["layout"].get(tag, 0)
                sheets = p.get("sheets", 0)
                total_produced += ups * sheets

        excess = total_produced - demand[tag]
        excess_percent = round((excess / demand[tag]) * 100, 2) if demand[tag] else 0

        row["Total Produced QTY"] = total_produced
        row["Excess"] = max(0, excess)
        row["Excess %"] = f"{max(0, excess_percent)}%"
        rows.append(row)
        sl += 1

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    total_row = {
        "SL": "📊",
        "Tag": "TOTAL",
        "Original QTY": df["Original QTY"].sum(),
        "Produced (+Add-on)": df["Produced (+Add-on)"].sum(),
    }

    for idx, p in enumerate(plates):
        col_name = f"Plate {p['name']}" if "name" in p else f"Plate {idx+1}"
        if col_name in df.columns:
            total_row[col_name] = df[col_name].sum()
        else:
            total_row[col_name] = 0

    total_row["Total Produced QTY"] = df["Total Produced QTY"].sum()
    total_excess = df["Excess"].sum()
    total_row["Excess"] = total_excess
    
    total_produced_qty = total_row["Total Produced QTY"]
    total_excess_percent = round((total_excess / total_produced_qty) * 100, 2) if total_produced_qty > 0 else 0
    total_row["Excess %"] = f"{total_excess_percent}%"

    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
    return df


def generate_pdf_report(plates: list, demand: dict, original_qty: dict,
                        algo_name: str, waste_percent: float,
                        styles_dict: dict = None, colors_dict: dict = None, 
                        sizes_dict: dict = None, job_number: str = "") -> BytesIO | None:
    """Generate professional PDF report with Style, Color, Size columns and Job Number"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
    except ImportError:
        return None

    if styles_dict is None: styles_dict = {}
    if colors_dict is None: colors_dict = {}
    if sizes_dict is None: sizes_dict = {}

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=landscape(A4),
            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
        )
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'],
            fontSize=14, alignment=TA_CENTER, 
            textColor=colors.HexColor('#667eea'),
            spaceAfter=4
        )
        job_style = ParagraphStyle(
            'JobStyle', parent=styles['Heading2'],
            fontSize=12, alignment=TA_CENTER,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=8
        )
        subtitle_style = ParagraphStyle(
            'CustomSubtitle', parent=styles['Normal'],
            fontSize=9, alignment=TA_CENTER, 
            textColor=colors.grey,
            spaceAfter=12
        )
        footer_style = ParagraphStyle(
            'Footer', parent=styles['Normal'],
            fontSize=8, alignment=TA_CENTER, 
            textColor=colors.grey,
            spaceTop=12
        )

        story = []
        
        story.append(Paragraph("📊 Plate Ratio System - Ratio Report", title_style))
        if job_number:
            story.append(Paragraph(f"🔢 Job Number: {job_number}", job_style))
        story.append(Paragraph(
            f"Algorithm: {algo_name} | Waste: {waste_percent}% | "
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            subtitle_style
        ))
        story.append(Spacer(1, 10))

        header_row = ["SL", "Style", "Color", "Size", "Original", "With Add-on"]
        for p in plates:
            header_row.append(f"Plate {p['name']}")
        header_row.extend(["Total Prod.", "Excess", "Excess %"])
        
        summary_data = [header_row]
        
        sl = 1
        for tag in demand.keys():
            style = styles_dict.get(tag, "N/A")
            color = colors_dict.get(tag, "N/A")
            size = sizes_dict.get(tag, "N/A")
            
            row = [str(sl), style, color, size, 
                   str(original_qty.get(tag, 0)), str(demand[tag])]
            
            total_produced = 0
            for p in plates:
                ups = p["layout"].get(tag, 0)
                row.append(str(ups))
                total_produced += ups * p["sheets"]
            
            excess = total_produced - demand[tag]
            excess_percent = f"{round((excess / demand[tag]) * 100, 2) if demand[tag] else 0}%"
            row.extend([str(total_produced), str(excess), excess_percent])
            summary_data.append(row)
            sl += 1
        
        total_row = ["📊", "TOTAL", "", "", 
                     str(sum(original_qty.values())), str(sum(demand.values()))]
        
        total_produced_sum = 0
        for p in plates:
            plate_total = 0
            for tag in demand:
                plate_total += p["layout"].get(tag, 0) * p["sheets"]
            total_row.append(str(plate_total))
            total_produced_sum += plate_total
        
        total_excess_sum = total_produced_sum - sum(demand.values())
        total_excess_percent = (
            f"{round((total_excess_sum / total_produced_sum) * 100, 2) if total_produced_sum > 0 else 0}%"
        )
        total_row.extend([str(total_produced_sum), str(total_excess_sum), total_excess_percent])
        summary_data.append(total_row)
        
        main_table = Table(summary_data, repeatRows=1)
        
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 6),
            ('ALIGN', (0, 1), (-1, -2), 'CENTER'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        for i in range(1, len(summary_data) - 1):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa')))
        
        main_table.setStyle(TableStyle(table_style))
        story.append(main_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph("🧾 Plate Configuration Details", 
                              ParagraphStyle('SubHeader', parent=styles['Heading2'],
                                           fontSize=11, alignment=TA_CENTER,
                                           textColor=colors.HexColor('#667eea'))))
        story.append(Spacer(1, 8))
        
        plate_data = [["SL", "Plate ID", "Sheets", "Total UPS"]]
        for idx, p in enumerate(plates, 1):
            plate_data.append([
                str(idx), 
                p["name"], 
                str(p["sheets"]), 
                str(sum(p["layout"].values()))
            ])
        
        plate_table = Table(plate_data)
        plate_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(plate_table)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(
            f"This Report Generated by Ovi's Plate Ratio System | Job: {job_number if job_number else 'N/A'} | All Rights Reserved",
            footer_style
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        return None


# ================================================================
# V27 ALGORITHM IMPLEMENTATION (🎨 MAX PLATES ENFORCED)
# ================================================================
def v27_optimized(demand_dict, plate_capacity=60, max_plates=10, iterations=50):
    """
    V27 - Optimized Version
    Inspired by Ovi's Manual Excel Workflow
    """
    
    def calculate_waste(plates, demand):
        total_produced = 0
        total_demand = sum(demand.values())
        
        for plate in plates:
            for tag, ups in plate["layout"].items():
                total_produced += ups * plate["sheets"]
        
        if total_produced == 0:
            return 100.0
        
        waste = total_produced - total_demand
        return (waste / total_produced) * 100
    
    def create_layout(remaining, capacity):
        """Smart UPS Distribution"""
        active = {k: v for k, v in remaining.items() if v > 0}
        if not active:
            return {}
        
        total_active = sum(active.values())
        layout = {}
        used = 0
        
        # Proportional distribution
        for tag, qty in sorted(active.items(), key=lambda x: x[1], reverse=True):
            if used >= capacity:
                break
            ups = max(1, int((qty / total_active) * capacity))
            ups = min(ups, capacity - used)
            if ups > 0:
                layout[tag] = ups
                used += ups
        
        # Fill remaining
        while used < capacity and active:
            best = max(active, key=lambda t: remaining[t] / (layout.get(t, 1) + 1))
            layout[best] = layout.get(best, 0) + 1
            used += 1
        
        return layout
    
    def simulate_with_sheets(sheets):
        """Simulate one scenario with given sheets"""
        remaining = demand_dict.copy()
        plates = []
        plate_count = 0
        
        while plate_count < max_plates and any(v > 0 for v in remaining.values()):
            # Create layout
            layout = create_layout(remaining, plate_capacity)
            if not layout:
                break
            
            # Calculate sheets for this plate
            if plate_count == max_plates - 1:  # Last plate
                needed = []
                for tag, ups in layout.items():
                    if ups > 0 and remaining.get(tag, 0) > 0:
                        needed.append(ceil(remaining[tag] / ups))
                current_sheets = max(needed) if needed else sheets
            else:
                current_sheets = sheets
            
            # Apply layout
            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * current_sheets))
            
            plates.append({
                "name": plate_name(plate_count + 1),
                "layout": layout,
                "sheets": current_sheets
            })
            
            plate_count += 1
        
        return plates
    
    # ================================================================
    # MAIN LOGIC
    # ================================================================
    
    total_qty = sum(demand_dict.values())
    capacity_per_round = max_plates * plate_capacity
    estimated_sheets = ceil(total_qty / capacity_per_round)
    
    # Generate candidate sheets
    candidate_sheets = []
    for i in range(-iterations//2, iterations//2 + 1):
        candidate = estimated_sheets + i
        if candidate >= 1:
            candidate_sheets.append(candidate)
    candidate_sheets = sorted(set(candidate_sheets))
    
    # Test each candidate
    best_plates = None
    best_waste = float('inf')
    best_sheets = None
    
    for sheets in candidate_sheets:
        plates = simulate_with_sheets(sheets)
        if plates:
            waste = calculate_waste(plates, demand_dict)
            if waste < best_waste:
                best_waste = waste
                best_plates = plates
                best_sheets = sheets
    
    return {
        "plates": ensure_demand_met(best_plates, demand_dict),
        "waste_percent": best_waste,
        "sheets_used": best_sheets,
        "total_plates": len(best_plates) if best_plates else 0,
        "candidates_tested": len(candidate_sheets)
    }

# ================== CONFIGURATION ==================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n = st.number_input("🏷️ Number of Items", 1, 500, 3)
with col2:
    cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 60)
with col3:
    maxp = st.number_input("🎨 Max Plates", 1, 50, 3) # Default value updated to 3 as requested
with col4:
    addon = st.number_input("📈 Add-on (%)", 0.0, 50.0, 0.0, step=0.5)
with col5:
    job_number = st.text_input(
        "🔢 Job Number", 
        value="",
        placeholder="e.g., JOB-001",
        help="Enter a job number for tracking (optional)"
    )
    if not job_number:
        job_number = f"JOB-{datetime.now().strftime('%Y%m%d_%H%M')}"

st.markdown('</div>', unsafe_allow_html=True)

st.session_state['job_number'] = job_number

# ================== INPUT MODE SELECTION ==================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Input Method</div>', unsafe_allow_html=True)

input_mode = st.radio(
    "Select Input Mode:",
    options=["✏️ Manual Input", "📂 Upload Excel File"],
    horizontal=True,
    index=0
)

st.markdown('</div>', unsafe_allow_html=True)

tags = []
styles = []
colors = []
sizes = []
qty = []

styles_dict = {}
colors_dict = {}
sizes_dict = {}
original_qty = {}
demand_dict = {}

# ================== MANUAL INPUT ==================
if input_mode == "✏️ Manual Input":
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Item Quantity Details (Manual)</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
    with col1: st.markdown("**SL**")
    with col2: st.markdown("**Style**")
    with col3: st.markdown("**Color**")
    with col4: st.markdown("**Size**")
    with col5: st.markdown("**Quantity**")
    
    st.markdown("---")
    
    for i in range(n):
        col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        
        with col1:
            st.markdown(f"**{i+1}**")
        with col2:
            style_val = st.text_input("Style", value=f"Style_{i+1}", key=f"style_{i}", label_visibility="collapsed")
        with col3:
            color_val = st.text_input("Color", value="Black", key=f"color_{i}", label_visibility="collapsed")
        with col4:
            size_val = st.text_input("Size", value=chr(83 + i % 4), key=f"size_{i}", label_visibility="collapsed")
        with col5:
            qty_val = st.number_input("Quantity", min_value=0, value=1000 * (i+1), step=100, key=f"qty_manual_{i}", label_visibility="collapsed")
        
        style_display = style_val.strip() if style_val.strip() else "N/A"
        color_display = color_val.strip() if color_val.strip() else "N/A"
        size_display = size_val.strip() if size_val.strip() else "N/A"
        
        tag = f"Item_{i+1}_{style_display}_{size_display}"
        tags.append(tag)
        qty.append(qty_val)
        
        styles_dict[tag] = style_display
        colors_dict[tag] = color_display
        sizes_dict[tag] = size_display
        original_qty[tag] = qty_val
        demand_dict[tag] = int(qty_val * (1 + addon / 100))
        
    st.markdown('</div>', unsafe_allow_html=True)

# ================== EXCEL UPLOAD ==================
else:
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📂 Item Quantity Details (Excel Upload)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        try:
            # Dynamic Row skipping fixed to start after row 29 metadata
            df_xl = pd.read_excel(uploaded_file, skiprows=29)
            st.success("Excel File Loaded Successfully!")
            st.dataframe(df_xl.head(), use_container_width=True)
            
            columns_list = list(df_xl.columns)
            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1: style_col = st.selectbox("Select Style Column", columns_list, index=0 if "Style" not in columns_list else columns_list.index("Style"))
            with col_c2: color_col = st.selectbox("Select Color Column", columns_list, index=min(1, len(columns_list)-1) if "Color" not in columns_list else columns_list.index("Color"))
            with col_c3: size_col = st.selectbox("Select Size Column", columns_list, index=min(2, len(columns_list)-1) if "Size" not in columns_list else columns_list.index("Size"))
            with col_c4: qty_col = st.selectbox("Select Quantity Column", columns_list, index=min(3, len(columns_list)-1) if "Quantity" not in columns_list else columns_list.index("Quantity"))
            
            for index, row in df_xl.iterrows():
                st_val = str(row[style_col]).strip() if style_col in df_xl.columns else "N/A"
                cl_val = str(row[color_col]).strip() if color_col in df_xl.columns else "N/A"
                sz_val = str(row[size_col]).strip() if size_col in df_xl.columns else "N/A"
                q_val = int(row[qty_col]) if qty_col in df_xl.columns and pd.notnull(row[qty_col]) else 0
                
                tag = f"Item_{index+1}_{st_val}_{sz_val}"
                tags.append(tag)
                qty.append(q_val)
                
                styles_dict[tag] = st_val
                colors_dict[tag] = cl_val
                sizes_dict[tag] = sz_val
                original_qty[tag] = q_val
                demand_dict[tag] = int(q_val * (1 + addon / 100))
        except Exception as e:
            st.error(f"Error parsing Excel: {str(e)}")
            
    st.markdown('</div>', unsafe_allow_html=True)


# ================== EXECUTION & OPTIMIZATION ==================
if tags and sum(qty) > 0:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    if st.button("🚀 Calculate V27 Optimal Ratios", type="primary"):
        with st.spinner("Executing Algorithm V27 Simulation..."):
            algo_res = algo_v27_dynamic_step_down_optimization(demand_dict, cap, int(maxp))
            
            if algo_res and algo_res["plates"]:
                final_plates = ensure_demand_met(algo_res["plates"], demand_dict)
                w_percent = calculate_waste_percent(final_plates, demand_dict)
                
                st.session_state['v27_plates'] = final_plates
                st.session_state['v27_waste'] = w_percent
                st.session_state['v27_produced'] = algo_res["produced"]
                st.session_state['v27_factor'] = algo_res["factor_percentage"]
                st.session_state['calculated'] = True
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================== RESULTS DISPLAY ==================
if st.session_state.get('calculated', False):
    plates = st.session_state['v27_plates']
    w_percent = st.session_state['v27_waste']
    factor = st.session_state['v27_factor']
    
    # 🌟 Performance Summary Cards
    st.markdown('<div class="best-algo">🎖️ Best Simulation Strategy Found: ' + factor + ' Scaling </div>', unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(plates)}</div><div class="metric-label">Total Plates Generated (Max Bounded)</div></div>', unsafe_allow_html=True)
    with c_m2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{w_percent}%</div><div class="metric-label">Total Material Waste</div></div>', unsafe_allow_html=True)
    with c_m3:
        total_sheets_run = sum(p["sheets"] for p in plates)
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_sheets_run}</div><div class="metric-label">Total Sheets To Print</div></div>', unsafe_allow_html=True)
        
    st.write("##")
    
    # Summary Table Display
    st.markdown('<div class="card"><div class="card-title">📊 Complete Production Layout Sheet</div>', unsafe_allow_html=True)
    df_summary = build_full_summary(plates, demand_dict, original_qty)
    
    # Replace Technical internal tags with beautiful style labels for presentation
    if not df_summary.empty:
        df_summary['Tag'] = df_summary['Tag'].apply(lambda x: styles_dict.get(x, x) if x != "TOTAL" else "TOTAL")
    
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Plate Layout Breakdowns
    st.markdown('<div class="card"><div class="card-title">🛠️ Individual Plate Matrix Detail</div>', unsafe_allow_html=True)
    for p in plates:
        with st.expander(f"📦 Plate {p['name']} — Print Run: {p['sheets']} Sheets", expanded=True):
            p_cols = st.columns(2)
            with p_cols[0]:
                st.write("**Ratio Layout (UPS Allocation per Size):**")
                display_layout = {sizes_dict.get(k, k): v for k, v in p["layout"].items() if v > 0}
                st.json(display_layout)
            with p_cols[1]:
                st.write("**Total Output Pieces from this Plate:**")
                display_prod = {sizes_dict.get(k, k): v for k, v in p["production"].items() if v > 0}
                st.json(display_prod)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF Export Section
    if REPORTLAB_AVAILABLE:
        st.markdown('<div class="card"><div class="card-title">📄 Export Professional Documents</div>', unsafe_allow_html=True)
        pdf_buffer = generate_pdf_report(plates, demand_dict, original_qty, "Algorithm V27 (Step-Down)", w_percent, styles_dict, colors_dict, sizes_dict, job_number)
        
        if pdf_buffer:
            st.download_button(
                "📥 Download Ratio Analysis PDF Report",
                pdf_buffer,
                f"{job_number}_V27_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
        © 2026 Plate Ratio System | Version 27 (Testing Edition)
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 8px 0;">
        Enterprise Production Optimization Framework • Manual Logic Injected • Production Ready
    </p>
</div>
""", unsafe_allow_html=True)
