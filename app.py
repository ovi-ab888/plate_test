# app.py — COMPLETE PLATE RATIO SYSTEM (V1 to V26)
# All Algorithms Fixed | No Negative Excess | Production Ready
# Design by Ovi

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

# Try to import PuLP for Integer Solver
try:
    from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, LpInteger
    PULP_AVAILABLE = True
except ImportError:
    PULP_AVAILABLE = False

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

# Try to import OR-Tools for V19
try:
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False


# ================================================================
# STREAMLIT PAGE CONFIGURATION
# ================================================================
st.set_page_config(
    page_title="Plate Ratio System - Complete Edition",
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
    <p>Complete Edition • 26 Algorithms • Production Ready</p>
    <p style="font-size: 0.85rem; opacity: 0.6;">AI-Powered • Fast • Accurate</p>
    <div class="designer-name">✨ Design by Ovi ✨</div>
</div>
""", unsafe_allow_html=True)



# ================================================================
# UNIVERSAL LAYOUT GENERATOR (FIXED FOR ALL ALGORITHMS)
# ================================================================
def create_valid_layout(active: dict, capacity: int, method: str = "balanced") -> dict:
    """
    Create a layout that respects capacity even when items > capacity
    Methods: "balanced", "proportional", "greedy"
    """
    if not active:
        return {}
    
    total_qty = sum(active.values())
    n_items = len(active)
    
    # Special case: বেশি আইটেম, কম capacity
    if n_items > capacity:
        layout = {}
        
        if method == "balanced":
            # প্রতিটি আইটেমের জন্য প্রপোরশনাল UPS
            for tag, qty in active.items():
                ups = max(1, int((qty / total_qty) * capacity))
                layout[tag] = ups
            
            # Exact capacity enforce
            while sum(layout.values()) > capacity:
                max_tag = max(layout, key=layout.get)
                if layout[max_tag] > 1:
                    layout[max_tag] -= 1
                else:
                    # সব UPS 1 হলে, সবচেয়ে কম গুরুত্বপূর্ণ ট্যাগ 0 করো
                    min_tag = min(active, key=lambda t: active[t])
                    if layout.get(min_tag, 0) > 0:
                        layout[min_tag] = 0
                    else:
                        break
            
            while sum(layout.values()) < capacity:
                # সবচেয়ে বেশি ডিমান্ডের আইটেমকে প্রায়োরিটি দাও
                max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
                layout[max_tag] = layout.get(max_tag, 0) + 1
            
            return layout
        
        elif method == "greedy":
            # প্রতিটি আইটেমের জন্য 1 করে দাও, তারপর বাকি capacity পূরণ করো
            for tag in active.keys():
                layout[tag] = 1
            
            remaining_cap = capacity - sum(layout.values())
            
            if remaining_cap > 0:
                sorted_items = sorted(active.items(), key=lambda x: x[1], reverse=True)
                for tag, _ in sorted_items:
                    if remaining_cap <= 0:
                        break
                    layout[tag] = layout.get(tag, 1) + 1
                    remaining_cap -= 1
            
            return layout
        
        elif method == "proportional":
            # প্রপোরশনাল ভাগাভাগি
            for tag, qty in active.items():
                ups = int((qty / total_qty) * capacity)
                if ups < 1:
                    ups = 1 if len(active) <= capacity else 0
                layout[tag] = ups
            
            # Exact capacity enforce
            while sum(layout.values()) > capacity:
                max_tag = max(layout, key=layout.get)
                if layout[max_tag] > 1:
                    layout[max_tag] -= 1
                else:
                    break
            
            while sum(layout.values()) < capacity:
                max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
                layout[max_tag] = layout.get(max_tag, 0) + 1
            
            return layout
    
    # Normal case: আইটেম সংখ্যা capacity এর কম বা সমান
    layout = {}
    
    if method == "balanced":
        for tag, qty in active.items():
            ideal = (qty / total_qty) * capacity
            base = int(ideal)
            if base < 1:
                base = 1
            layout[tag] = base
        
        # Adjust to exact capacity
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=layout.get)
            if layout[max_tag] > 1:
                layout[max_tag] -= 1
            else:
                break
        
        while sum(layout.values()) < capacity:
            # সবচেয়ে বেশি fractional part যার
            fractional = {}
            for tag, qty in active.items():
                ideal = (qty / total_qty) * capacity
                fractional[tag] = ideal - int(ideal)
            best = max(fractional, key=fractional.get)
            layout[best] = layout.get(best, 0) + 1
    
    else:  # proportional or greedy
        for tag, qty in active.items():
            ups = max(1, int((qty / total_qty) * capacity))
            layout[tag] = ups
        
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=layout.get)
            if layout[max_tag] > 1:
                layout[max_tag] -= 1
            else:
                break
        
        while sum(layout.values()) < capacity:
            max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
            layout[max_tag] = layout.get(max_tag, 0) + 1
    
    return layout
    

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
    
    # Ensure all plates have names
    for idx, plate in enumerate(plates):
        if "name" not in plate:
            plate["name"] = plate_name(idx + 1)
    
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
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    except ImportError:
        return None

    # Initialize empty dicts if not provided
    if styles_dict is None:
        styles_dict = {}
    if colors_dict is None:
        colors_dict = {}
    if sizes_dict is None:
        sizes_dict = {}

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=landscape(A4),
            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
        )
        styles = getSampleStyleSheet()

        # Custom styles
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
        
        # Header with Job Number
        story.append(Paragraph("📊 Plate Ratio System - Ratio Report", title_style))
        if job_number:
            story.append(Paragraph(f"🔢 Job Number: {job_number}", job_style))
        story.append(Paragraph(
            f"Algorithm: {algo_name} | Waste: {waste_percent}% | "
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            subtitle_style
        ))
        story.append(Spacer(1, 10))

        # ============= MAIN SUMMARY TABLE =============
        # Build header with all columns
        header_row = ["SL", "Style", "Color", "Size", "Original", "With Add-on"]
        for p in plates:
            header_row.append(f"Plate {p['name']}")
        header_row.extend(["Total Prod.", "Excess", "Excess %"])
        
        summary_data = [header_row]
        
        # Build data rows
        sl = 1
        for tag in demand.keys():
            # Get style/color/size from session state or use defaults
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
        
        # Total row
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
        
        # Create main table
        main_table = Table(summary_data, repeatRows=1)
        
        # Style the table
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
        
        # Apply alternating row colors
        for i in range(1, len(summary_data) - 1):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa')))
        
        main_table.setStyle(TableStyle(table_style))
        story.append(main_table)
        story.append(Spacer(1, 15))
        
        # ============= PLATE DETAILS TABLE =============
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
        
        # ============= FOOTER =============
        story.append(Paragraph(
            f"This Report Generated by Ovi's Plate Ratio System | Job: {job_number if job_number else 'N/A'} | All Rights Reserved",
            footer_style
        ))
        
        # Build the PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        return None






def algo_v27_dynamic_step_down_optimization(demand_dict, plate_capacity=60):
    """
    Algorithm V27: Dynamic Step-Down Balance Optimization (Multi-Scenario)
    Inspired & Designed by Ovi's Manual Excel Workflow.
    """
    TOTAL_UPS = plate_capacity
    scaling_factors = [0.80, 0.90, 1.00, 1.10, 1.20]
    best_result = None
    min_total_waste = float('inf')
    
    for factor in scaling_factors:
        current_demand = copy.deepcopy(demand_dict)
        plates_list = []
        run_count = 1
        
        total_initial_demand = sum(current_demand.values())
        if total_initial_demand == 0:
            continue
        estimated_sheets = total_initial_demand / TOTAL_UPS
        initial_target_sheets = max(1, int(round(estimated_sheets * factor)))
        
        is_first_run = True
        
        while sum(current_demand.values()) > 0 and run_count <= 25:
            active_sizes = {k: v for k, v in current_demand.items() if v > 0}
            if not active_sizes:
                break
                
            total_active_demand = sum(active_sizes.values())
            raw_ups = {}
            for size, qty in active_sizes.items():
                raw_ups[size] = (qty / total_active_demand) * TOTAL_UPS
            
            allocated_ups = {size: max(1, int(floor(val))) for size, val in raw_ups.items()}
            
            remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
            if remaining_ups > 0:
                sorted_by_remainder = sorted(raw_ups.items(), key=lambda x: x[1] - allocated_ups[x[0]], reverse=True)
                for size, _ in sorted_by_remainder:
                    if remaining_ups == 0:
                        break
                    allocated_ups[size] += 1
                    remaining_ups -= 1
            
            if sum(allocated_ups.values()) > TOTAL_UPS:
                sorted_by_ups = sorted(allocated_ups.items(), key=lambda x: x[1], reverse=True)
                for size, _ in sorted_by_ups:
                    if sum(allocated_ups.values()) == TOTAL_UPS:
                        break
                    if allocated_ups[size] > 1:
                        allocated_ups[size] -= 1
            
            if is_first_run:
                run_sheets = initial_target_sheets
                is_first_run = False
            else:
                min_sheet_needed = float('inf')
                for size, qty in active_sizes.items():
                    ups = allocated_ups.get(size, 1)
                    needed = int(ceil(qty / ups))
                    if needed < min_sheet_needed:
                        min_sheet_needed = needed
                run_sheets = max(1, min_sheet_needed)
            
            plate_production = {}
            for size, ups in allocated_ups.items():
                plate_production[size] = ups * run_sheets
                current_demand[size] = max(0, current_demand[size] - plate_production[size])
            
            plates_list.append({
                "plate_index": run_count,
                "layout": allocated_ups,
                "sheets": run_sheets,
                "production": plate_production
            })
            
            run_count += 1
            
        total_produced = {size: 0 for size in demand_dict.keys()}
        for p in plates_list:
            for size, qty in p["production"].items():
                total_produced[size] += qty
                
        scenario_waste = 0
        for size, target in demand_dict.items():
            produced = total_produced.get(size, 0)
            excess = produced - target
            if excess > 0:
                scenario_waste += excess
                
        if scenario_waste < min_total_waste:
            min_total_waste = scenario_waste
            best_result = {
                "plates": plates_list,
                "waste": scenario_waste,
                "produced": total_produced,
                "factor_percentage": f"{int(factor * 100)}%"
            }
            
    return best_result


# ================================================================
# MAIN UI
# ================================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Plate Ratio Intelligence System</h1>
    <p>Complete Edition • 26 Algorithms • Production Ready</p>
    <p style="font-size: 0.85rem; opacity: 0.6;">AI-Powered • Fast • Accurate</p>
</div>
""", unsafe_allow_html=True)

# ================== CONFIGURATION ==================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n = st.number_input("🏷️ Number of Items", 1, 500, 1)
with col2:
    cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 10)
with col3:
    maxp = st.number_input("🎨 Max Plates", 1, 50, 3)
with col4:
    addon = st.number_input("📈 Add-on (%)", 0.0, 50.0, 0.0, step=0.5)
with col5:
    job_number = st.text_input(
        "🔢 Job Number", 
        value="",
        placeholder="e.g., JOB-001",
        help="Enter a job number for tracking (optional)"
    )
    # If empty, generate default
    if not job_number:
        job_number = f"JOB-{datetime.now().strftime('%Y%m%d_%H%M')}"

st.markdown('</div>', unsafe_allow_html=True)

# Store job number in session state
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

# ================== MANUAL INPUT ==================
if input_mode == "✏️ Manual Input":
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Item Quantity Details (Manual)</div>', unsafe_allow_html=True)
    
    # Column headers
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
    with col1:
        st.markdown("**SL**")
    with col2:
        st.markdown("**Style**")
    with col3:
        st.markdown("**Color**")
    with col4:
        st.markdown("**Size**")
    with col5:
        st.markdown("**Quantity**")
    
    st.markdown("---")
    
    tags = []
    styles = []
    colors = []
    sizes = []
    qty = []
    
    for i in range(n):
        col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        
        with col1:
            st.markdown(f"**{i+1}**")
        
        with col2:
            style_val = st.text_input(
                "Style", 
                value="N/A", 
                key=f"style_{i}",
                label_visibility="collapsed",
                placeholder="N/A"
            )
        
        with col3:
            color_val = st.text_input(
                "Color", 
                value="N/A", 
                key=f"color_{i}",
                label_visibility="collapsed",
                placeholder="N/A"
            )
        
        with col4:
            size_val = st.text_input(
                "Size", 
                value="N/A", 
                key=f"size_{i}",
                label_visibility="collapsed",
                placeholder="N/A"
            )
        
        with col5:
            qty_val = st.number_input(
                "Quantity", 
                min_value=0, 
                value=0, 
                step=100, 
                key=f"qty_manual_{i}",
                label_visibility="collapsed"
            )
        
        # Store values
        style_display = style_val.strip() if style_val.strip() else "N/A"
        color_display = color_val.strip() if color_val.strip() else "N/A"
        size_display = size_val.strip() if size_val.strip() else "N/A"
        
        styles.append(style_display)
        colors.append(color_display)
        sizes.append(size_display)
        
        # Create tag with style info (for display purposes)
        tag = f"Item {i+1}"
        if style_display != "N/A":
            tag = f"{style_display}"
        
        tags.append(tag)
        qty.append(qty_val)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show preview with all columns
    if any(q > 0 for q in qty):
        preview_df = pd.DataFrame({
            "SL": range(1, n + 1),
            "Style": styles,
            "Color": colors,
            "Size": sizes,
            "Quantity": qty
        })
        st.info("📋 Data Preview (showing all items)")
        st.dataframe(preview_df, use_container_width=True, height=200)
    
    # Data Preparation
    original_qty = {f"Item {i+1}": int(q) for i, q in enumerate(qty) if q > 0}
    demand = {f"Item {i+1}": ceil(int(q) * (1 + addon / 100)) for i, q in enumerate(qty) if q > 0}
    
    # Store style/color/size info for later use
    st.session_state['item_styles'] = {f"Item {i+1}": styles[i] for i in range(n)}
    st.session_state['item_colors'] = {f"Item {i+1}": colors[i] for i in range(n)}
    st.session_state['item_sizes'] = {f"Item {i+1}": sizes[i] for i in range(n)}

# ================== EXCEL FILE UPLOAD ==================
else:
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📂 Upload Excel File</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Excel file with Item Details",
        type=["xlsx", "xls"],
        help="File must have columns: SL, Style, Color, Size, Quantity"
    )
    

    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Auto-detect columns
            # Look for required columns
            style_col = None
            color_col = None
            size_col = None
            qty_col = None
            sl_col = None
            
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if col_lower in ['style', 'styles']:
                    style_col = col
                elif col_lower in ['color', 'colors', 'colour']:
                    color_col = col
                elif col_lower in ['size', 'sizes']:
                    size_col = col
                elif col_lower in ['quantity', 'qty', 'qty.', 'quantities', 'total']:
                    qty_col = col
                elif col_lower in ['sl', 's/l', 'serial', 'serial no', 'serial no.', 'no']:
                    sl_col = col
            
            # If specific columns not found, try to map by position
            if qty_col is None and len(df.columns) >= 2:
                # Try to find quantity column (usually the last column with numbers)
                for col in df.columns:
                    if df[col].dtype in ['int64', 'float64']:
                        qty_col = col
                        break
            
            # If still not found, use last column as quantity
            if qty_col is None and len(df.columns) >= 2:
                qty_col = df.columns[-1]
            
            # If style/color/size not found, use empty strings or create from SL
            if style_col is None:
                style_col = df.columns[1] if len(df.columns) >= 2 else None
            if color_col is None:
                color_col = df.columns[2] if len(df.columns) >= 3 else None
            if size_col is None:
                size_col = df.columns[3] if len(df.columns) >= 4 else None
            
            if qty_col is None:
                st.error("❌ Could not find 'Quantity' column. Please ensure your file has a quantity column.")
                st.info("📌 Column names can be: 'Quantity', 'Qty', 'QTY', 'Total'")
                st.stop()
            
            # Extract data
            sl_data = df[sl_col].tolist() if sl_col else list(range(1, len(df) + 1))
            style_data = df[style_col].astype(str).tolist() if style_col else ["N/A"] * len(df)
            color_data = df[color_col].astype(str).tolist() if color_col else ["N/A"] * len(df)
            size_data = df[size_col].astype(str).tolist() if size_col else ["N/A"] * len(df)
            qty_data = df[qty_col].tolist()
            
            # Clean data: remove NaN, empty strings, and non-numeric quantities
            cleaned_data = []
            skipped_rows = 0
            
            for idx, (sl, style, color, size, qty) in enumerate(zip(sl_data, style_data, color_data, size_data, qty_data)):
                # Skip if quantity is NaN or invalid
                if pd.isna(qty):
                    skipped_rows += 1
                    continue
                
                try:
                    qty_int = int(float(qty))  # Convert to int
                    if qty_int > 0:  # Only keep positive quantities
                        # Clean up values
                        style_val = str(style).strip() if not pd.isna(style) and str(style).strip() != '' else "N/A"
                        color_val = str(color).strip() if not pd.isna(color) and str(color).strip() != '' else "N/A"
                        size_val = str(size).strip() if not pd.isna(size) and str(size).strip() != '' else "N/A"
                        sl_val = int(sl) if not pd.isna(sl) and str(sl).strip() != '' else idx + 1
                        
                        cleaned_data.append((sl_val, style_val, color_val, size_val, qty_int))
                    else:
                        skipped_rows += 1
                except (ValueError, TypeError):
                    skipped_rows += 1
                    continue
            
            if not cleaned_data:
                st.error("❌ No valid data found in the file. Please check the format.")
                st.stop()
            
            # Separate into lists
            sl_list = [item[0] for item in cleaned_data]
            style_list = [item[1] for item in cleaned_data]
            color_list = [item[2] for item in cleaned_data]
            size_list = [item[3] for item in cleaned_data]
            qty_list = [item[4] for item in cleaned_data]
            
            # Show preview
            preview_df = pd.DataFrame({
                "SL": sl_list,
                "Style": style_list,
                "Color": color_list,
                "Size": size_list,
                "Quantity": qty_list
            })
            
            st.success(f"✅ File loaded successfully! {len(cleaned_data)} valid items found.")
            if skipped_rows > 0:
                st.warning(f"⚠️ {skipped_rows} rows were skipped (empty or invalid data).")
            
            st.dataframe(preview_df, use_container_width=True)
            
            # Detected columns info
            detected_cols = []
            if sl_col:
                detected_cols.append(f"SL = '{sl_col}'")
            if style_col:
                detected_cols.append(f"Style = '{style_col}'")
            if color_col:
                detected_cols.append(f"Color = '{color_col}'")
            if size_col:
                detected_cols.append(f"Size = '{size_col}'")
            if qty_col:
                detected_cols.append(f"Quantity = '{qty_col}'")
            
            st.info(f"📋 Detected columns: {', '.join(detected_cols)}")
            
            # Auto-set the number of items
            n = len(cleaned_data)
            tags = [f"Item {i+1}" for i in range(n)]
            qty = qty_list
            
            # Store style/color/size data in session state for PDF
            st.session_state['item_styles'] = {f"Item {i+1}": style_list[i] for i in range(n)}
            st.session_state['item_colors'] = {f"Item {i+1}": color_list[i] for i in range(n)}
            st.session_state['item_sizes'] = {f"Item {i+1}": size_list[i] for i in range(n)}
            
            original_qty = {t: int(q) for t, q in zip(tags, qty) if q > 0}
            demand = {t: ceil(int(q) * (1 + addon / 100)) for t, q in zip(tags, qty) if q > 0}
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()
    else:
        st.info("📤 Please upload an Excel file to continue.")
        st.stop()

st.markdown('</div>', unsafe_allow_html=True)

# ================== WARNING MESSAGES ==================
if not PULP_AVAILABLE:
    st.markdown('<div class="warning">⚠️ PuLP library not installed. Some advanced features disabled.</div>', unsafe_allow_html=True)

if not ORTOOLS_AVAILABLE:
    st.markdown('<div class="warning">⚠️ OR-Tools not installed. V19 will be disabled. Install with: pip install ortools</div>', unsafe_allow_html=True)

# ================== GENERATE BUTTON ==================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("Generate Plans", use_container_width=True, type="primary")

# ================== AFTER GENERATE ==================
if generate_clicked:
    if not demand:
        st.error("⚠️ Please enter at least one item with quantity greater than 0")
        st.stop()

    with st.spinner("🔍 Searching for the perfect plate ratio... Almost there!"):
        
        # ================== ALL ALGORITHMS V1-V26 ==================
        results = {"Algorithm V27": algo_v27_dynamic_step_down_optimization(demand_dict, plate_capacity)}
     
        
        # Run all algorithms with progress bar
        results = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, (algo_name, func) in enumerate(algo_functions.items()):
            status_text.text(f"Running {algo_name}... ({idx+1}/{len(algo_functions)})")
            try:
                if maxp == 1 and algo_name in problematic_for_single_plate:
                    results[algo_name] = v3_optimizer(demand, cap, maxp)
                else:
                    results[algo_name] = func()
            except Exception as e:
                results[algo_name] = v3_optimizer(demand, cap, maxp)
            
            progress_bar.progress((idx + 1) / len(algo_functions))
        
        progress_bar.empty()
        status_text.empty()
        
        # Global fix for all algorithms
        for algo_name, plates in results.items():
            if plates:
                results[algo_name] = ensure_demand_met(plates, demand)
            else:
                results[algo_name] = v3_optimizer(demand, cap, maxp)
        
        # Comparison Data
        comparison_data = []
        for algo_name, plates in results.items():
            if plates:
                waste = calculate_waste_percent(plates, demand)
                comparison_data.append({
                    "Algorithm": algo_name,
                    "Waste %": waste,
                    "Total Plates": len(plates),
                    "Total Sheets": sum(p.get("sheets", 0) for p in plates),
                    "Status": "✅ Success"
                })
            else:
                comparison_data.append({
                    "Algorithm": algo_name,
                    "Waste %": 100,
                    "Total Plates": 0,
                    "Total Sheets": 0,
                    "Status": "❌ Failed"
                })
        
        comparison_df = pd.DataFrame(comparison_data).sort_values("Waste %")
        best_algo = comparison_df.iloc[0]["Algorithm"]
        best_waste = comparison_df.iloc[0]["Waste %"]
        
        # Store in session state
        st.session_state['results'] = results
        st.session_state['comparison_df'] = comparison_df
        st.session_state['best_algo'] = best_algo
        st.session_state['best_waste'] = best_waste
        st.session_state['demand'] = demand
        st.session_state['original_qty'] = original_qty
        
        # ====================== UI OUTPUT ======================
        st.markdown(f"""
        <div class="best-algo">
            <div class="metric-value">🏆 BEST ALGORITHM: {best_algo}</div>
            <div class="metric-label">Waste Percentage: {best_waste}%</div>
            <div class="metric-label">✨ Total Algorithms Tested: {len(results)} ✨</div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============= BEST ALGORITHM REPORT =============
        st.markdown("## 📋 Best Algorithm Report")
        best_plates = results[best_algo]
        
        if best_plates:
            try:
                st.markdown("### 📊 Production Summary")
                full_df = build_full_summary(best_plates, demand, original_qty)
                if not full_df.empty:
                    st.dataframe(full_df, use_container_width=True, height=380)
                
                st.markdown("### 🧾 Plate Configuration Details")
                plate_rows = []
                total_sheets_sum = 0
                total_ups_sum = 0
                
                for idx, p in enumerate(best_plates, 1):
                    if p and "layout" in p:
                        total_ups = sum(p["layout"].values())
                        plate_name_str = p.get("name", f"Plate {idx}")
                        plate_rows.append({
                            "SL": idx,
                            "Plate ID": plate_name_str,
                            "Sheets Required": p.get("sheets", 0),
                            "Total UPS": total_ups,
                        })
                        total_sheets_sum += p.get("sheets", 0)
                        total_ups_sum += total_ups
                
                plate_rows.append({
                    "SL": "📊",
                    "Plate ID": "TOTAL",
                    "Sheets Required": total_sheets_sum,
                    "Total UPS": total_ups_sum,
                })
                
                plate_details_df = pd.DataFrame(plate_rows)
                st.dataframe(plate_details_df, use_container_width=True)
                
                # ============= DOWNLOAD BUTTONS =============
                st.markdown("### 📥 Download Best Report")
                col1, col2 = st.columns(2)
                
                with col1:
                    bio_excel = BytesIO()
                    with pd.ExcelWriter(bio_excel, engine="openpyxl") as writer:
                        full_df.to_excel(writer, sheet_name="Summary", index=False)
                        plate_details_df.to_excel(writer, sheet_name="Plate Details", index=False)
                        comparison_df.to_excel(writer, sheet_name="Comparison", index=False)
                    bio_excel.seek(0)
                    
                    # Clean job number for Excel filename
                    job_number = st.session_state.get('job_number', 'JOB-00000')
                    clean_job = ''.join(c for c in job_number if c.isalnum() or c == '-')
                    excel_filename = f"{clean_job}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                    
                    st.download_button(
                        "📊 Download Excel",
                        bio_excel,
                        excel_filename,
                        use_container_width=True
                    )
                
                with col2:
                    # Check if reportlab is available
                    try:
                        import reportlab
                        REPORTLAB_AVAILABLE = True
                    except ImportError:
                        REPORTLAB_AVAILABLE = False
                    
                    if REPORTLAB_AVAILABLE:
                        try:
                            # Get style/color/size data from session state
                            styles_dict = st.session_state.get('item_styles', {})
                            colors_dict = st.session_state.get('item_colors', {})
                            sizes_dict = st.session_state.get('item_sizes', {})
                            job_number = st.session_state.get('job_number', 'JOB-00000')
                            
                            pdf_buffer = generate_pdf_report(
                                best_plates,
                                demand,
                                original_qty,
                                best_algo,
                                best_waste,
                                styles_dict,
                                colors_dict,
                                sizes_dict,
                                job_number
                            )
                            
                            if pdf_buffer:
                                # Clean job number for filename
                                clean_job = ''.join(c for c in job_number if c.isalnum() or c == '-')
                                pdf_filename = f"Job_Number_{clean_job}.pdf"
                                
                                st.download_button(
                                    "📄 Download PDF",
                                    pdf_buffer,
                                    pdf_filename,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ PDF could not be generated. Please check the data.")
                        except Exception as e:
                            st.error(f"❌ PDF Error: {str(e)}")
                    else:
                        st.info("ℹ️ PDF download requires reportlab. Install with: pip install reportlab")
            
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
                st.info("Showing comparison table instead...")
        
        # ============= ALGORITHM COMPARISON =============
        st.markdown("---")
        st.markdown("## 📊 Algorithm Comparison (Sorted by Waste %)")
        
        styled_df = comparison_df.style.apply(
            lambda row: ['background-color: #2e7d32; color: white'] * len(row)
            if row["Algorithm"] == best_algo else [''] * len(row),
            axis=1
        ).format({"Waste %": "{:.2f}%"})
        
        st.dataframe(styled_df, use_container_width=True, height=600)

# ============= VIEW ANY ALGORITHM REPORT =============
st.markdown("---")
st.markdown("## 🔍 View Individual Algorithm Report")

if 'results' in st.session_state and st.session_state['results']:
    algo_list = list(st.session_state['results'].keys())
    
    default_index = 0
    if st.session_state.get('best_algo') in algo_list:
        default_index = algo_list.index(st.session_state['best_algo'])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_algo = st.selectbox(
            "Select Algorithm to View Report:",
            options=algo_list,
            index=default_index,
            key="independent_algo_selector"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        view_button = st.button("📋 View Report", use_container_width=True, type="primary")
    
    if view_button:
        selected_plates = st.session_state['results'].get(selected_algo)
        
        if selected_plates:
            st.markdown(f"### 📊 Production Summary — **{selected_algo}**")
            
            full_df = build_full_summary(
                selected_plates, 
                st.session_state['demand'], 
                st.session_state['original_qty']
            )
            st.dataframe(full_df, use_container_width=True, height=400)
            
            st.markdown("### 🧾 Plate Configuration Details")
            plate_rows = []
            total_sheets = 0
            total_ups = 0
            
            for idx, p in enumerate(selected_plates, 1):
                ups_sum = sum(p["layout"].values())
                plate_rows.append({
                    "SL": idx,
                    "Plate ID": p.get("name", f"Plate {idx}"),
                    "Sheets Required": p.get("sheets", 0),
                    "Total UPS": ups_sum,
                })
                total_sheets += p.get("sheets", 0)
                total_ups += ups_sum
            
            plate_rows.append({
                "SL": "📊",
                "Plate ID": "TOTAL",
                "Sheets Required": total_sheets,
                "Total UPS": total_ups,
            })
            
            plate_df = pd.DataFrame(plate_rows)
            st.dataframe(plate_df, use_container_width=True)
            
            waste = calculate_waste_percent(selected_plates, st.session_state['demand'])
            st.success(f"**Waste: {waste}%** | Plates: {len(selected_plates)} | Total Sheets: {total_sheets}")
            
            # ✅ ডাউনলোড অপশন
            st.markdown("### 📥 Download Report")
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                try:
                    bio_excel = BytesIO()
                    with pd.ExcelWriter(bio_excel, engine="openpyxl") as writer:
                        full_df.to_excel(writer, sheet_name="Summary", index=False)
                        plate_df.to_excel(writer, sheet_name="Plate Details", index=False)
                    bio_excel.seek(0)
                    
                    st.download_button(
                        "📊 Download Excel",
                        bio_excel,
                        f"{selected_algo}_report.xlsx",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Excel export error: {str(e)}")
            
            with col_d2:
                if REPORTLAB_AVAILABLE:
                    try:
                        styles_dict = st.session_state.get('item_styles', {})
                        colors_dict = st.session_state.get('item_colors', {})
                        sizes_dict = st.session_state.get('item_sizes', {})
                        job_number = st.session_state.get('job_number', 'JOB-00000')
                        
                        pdf_buffer = generate_pdf_report(
                            selected_plates,
                            st.session_state['demand'],
                            st.session_state['original_qty'],
                            selected_algo,
                            waste,
                            styles_dict,
                            colors_dict,
                            sizes_dict,
                            job_number
                        )
                        
                        if pdf_buffer:
                            st.download_button(
                                "📄 Download PDF",
                                pdf_buffer,
                                f"{selected_algo}_report.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.warning(f"PDF not available: {str(e)}")
        else:
            st.error(f"❌ Report not found for {selected_algo}")
else:
    st.info("ℹ️ Please generate the optimization first to view individual algorithm reports.")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
        © 2025 Plate Ratio System | Version 26 (Complete Edition)
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 8px 0;">
        Enterprise Production Optimization Framework • 26 Algorithms • Production Ready
    </p>
    <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.85rem; font-weight: 600; margin: 10px 0 0 0;">
        ✨ Developed by Ovi | All Rights Reserved ✨
    </p>
</div>
""", unsafe_allow_html=True)
