# app.py — PLATE RATIO SYSTEM V2 (5 Algorithms for Large Dataset)
# Optimized for Large Datasets • Production Ready • No Shortfall Guaranteed
# Design by Ovi

import os
import copy
import random
import math
import string
from math import ceil, floor
from datetime import datetime
from io import BytesIO

os.environ["OPENBLAS_NUM_THREADS"] = "1"

import streamlit as st
import pandas as pd

# ================================================================
# LIBRARY IMPORTS & CHECKS FOR PDF GENERATION
# ================================================================
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
    page_title="Plate Ratio System V2 - 5 Algorithms",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ================================================================
# MODERN UI STYLING & CUSTOM CSS
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
    .main-header .subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 1.1rem;
        margin-top: 0.3rem;
    }
    .main-header .version {
        color: rgba(255,255,255,0.5);
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }
    .main-header .designer {
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
# HEADER DISPLAY
# ================================================================
st.markdown("""
<div class="main-header">
    <h1>🚀 Plate Ratio Intelligence System</h1>
    <div class="subtitle">V2 • 5 Optimized Algorithms • Large Dataset Ready</div>
    <div class="version">Smart Clustering • Multi-Variation • Global • AI Evolution • AI Mutation</div>
    <div class="designer">✨ Design by Ovi ✨</div>
</div>
""", unsafe_allow_html=True)


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def plate_name(n: int) -> str:
    """Convert number to Alphabetical ID (A, B, C... Z, AA...)"""
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
    """Calculate material waste percentage"""
    total_produced = 0
    total_demand = sum(demand.values())
    if total_demand == 0: 
        return 0.0

    for tag in demand:
        produced_qty = 0
        for p in plates:
            if p and "layout" in p:
                produced_qty += p["layout"].get(tag, 0) * p.get("sheets", 0)
        total_produced += produced_qty

    if total_produced == 0: 
        return 100.0
    waste = total_produced - total_demand
    return round(max(0, (waste / total_produced) * 100), 2)


# ================================================================
# 🔥 CRITICAL FIX: SMART SHORTFALL PREVENTION ENGINE 🔥
# ================================================================
def ensure_demand_met(plates: list, demand: dict) -> list:
    """Guarantees Total Produced QTY >= Demand for every single item without exception"""
    if not plates or not demand: 
        return plates
    
    # 1. Loop over each item to check for production shortages
    for tag in demand.keys():
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        
        if total_produced < demand[tag]:
            shortfall = demand[tag] - total_produced
            
            # Find the best plate that contains this item (highest UPS preferred)
            best_plate = None
            max_ups = 0
            
            for p in plates:
                ups = p["layout"].get(tag, 0)
                if ups > max_ups:
                    max_ups = ups
                    best_plate = p
                    
            # If item is found on a plate, increase sheets of that plate
            if best_plate and max_ups > 0:
                additional_sheets = ceil(shortfall / max_ups)
                best_plate["sheets"] += additional_sheets
            else:
                # Emergency fallback: If the item has 0 UPS on all plates, force 1 UPS on the last plate
                last_plate = plates[-1]
                last_plate["layout"][tag] = 1
                additional_sheets = ceil(shortfall / 1)
                last_plate["sheets"] += additional_sheets

    # 2. Recalculate full matrix data safely
    for p in plates:
        p["production"] = {tag: ups * p["sheets"] for tag, ups in p["layout"].items()}
        if "name" not in p:
            p["name"] = plate_name(p.get("plate_index", 1))
    
    return plates


def build_full_summary(plates: list, demand: dict, original_qty: dict) -> pd.DataFrame:
    """Generate final presentation data matrix"""
    rows = []
    sl = 1
    for tag in demand.keys():
        row = {
            "SL": sl, 
            "Tag": tag, 
            "Original QTY": original_qty.get(tag, 0), 
            "Produced (+Add-on)": demand[tag]
        }
        for p in plates:
            row[f"Plate {p['name']}"] = p["layout"].get(tag, 0)
            
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        excess = total_produced - demand[tag]
        row["Total Produced QTY"] = total_produced
        row["Excess"] = max(0, excess)
        row["Excess %"] = f"{round((excess / demand[tag]) * 100, 2) if demand[tag] else 0}%"
        rows.append(row)
        sl += 1

    df = pd.DataFrame(rows)
    total_row = {
        "SL": "📊", 
        "Tag": "TOTAL", 
        "Original QTY": df["Original QTY"].sum(), 
        "Produced (+Add-on)": df["Produced (+Add-on)"].sum()
    }
    for p in plates:
        total_row[f"Plate {p['name']}"] = df[f"Plate {p['name']}"].sum()
        
    total_row["Total Produced QTY"] = df["Total Produced QTY"].sum()
    total_row["Excess"] = df["Excess"].sum()
    
    total_prod_sum = total_row["Total Produced QTY"]
    total_row["Excess %"] = f"{round((df['Excess'].sum() / total_prod_sum) * 100, 2) if total_prod_sum else 0}%"
    
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)


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
            style = styles_dict.get(tag, "")
            color = colors_dict.get(tag, "")
            size = sizes_dict.get(tag, "")
            
            row = [str(sl), style, color, size, str(original_qty.get(tag, 0)), str(demand[tag])]
            
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
        
        total_row = ["📊", "TOTAL", "", "", str(sum(original_qty.values())), str(sum(demand.values()))]
        
        total_produced_sum = 0
        for p in plates:
            plate_total = 0
            for tag in demand:
                plate_total += p["layout"].get(tag, 0) * p["sheets"]
            total_row.append(str(plate_total))
            total_produced_sum += plate_total
        
        total_excess_sum = total_produced_sum - sum(demand.values())
        total_excess_percent = f"{round((total_excess_sum / total_produced_sum) * 100, 2) if total_produced_sum > 0 else 0}%"
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
            plate_data.append([str(idx), p["name"], str(p["sheets"]), str(sum(p["layout"].values()))])
        
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
        
        story.append(Paragraph(f"This Report Generated by Ovi's Plate Ratio System | Job: {job_number if job_number else 'N/A'} | All Rights Reserved", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception as e:
        return None


# ================================================================
# UNIVERSAL LAYOUT GENERATOR
# ================================================================
def create_valid_layout(active: dict, capacity: int, method: str = "balanced") -> dict:
    if not active: return {}
    total_qty = sum(active.values())
    n_items = len(active)
    
    if n_items > capacity:
        layout = {}
        if method == "balanced":
            for tag, qty in active.items():
                layout[tag] = max(1, int((qty / total_qty) * capacity))
            while sum(layout.values()) > capacity:
                max_tag = max(layout, key=layout.get)
                if layout[max_tag] > 1: layout[max_tag] -= 1
                else: break
            while sum(layout.values()) < capacity:
                max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
                layout[max_tag] = layout.get(max_tag, 0) + 1
            return layout
        elif method == "greedy":
            for tag in active.keys(): layout[tag] = 1
            remaining_cap = capacity - sum(layout.values())
            if remaining_cap > 0:
                sorted_items = sorted(active.items(), key=lambda x: x[1], reverse=True)
                for tag, _ in sorted_items:
                    if remaining_cap <= 0: break
                    layout[tag] = layout.get(tag, 1) + 1
                    remaining_cap -= 1
            return layout
        elif method == "proportional":
            for tag, qty in active.items():
                layout[tag] = max(1 if len(active) <= capacity else 0, int((qty / total_qty) * capacity))
            while sum(layout.values()) > capacity:
                max_tag = max(layout, key=layout.get)
                if layout[max_tag] > 1: layout[max_tag] -= 1
                else: break
            while sum(layout.values()) < capacity:
                max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
                layout[max_tag] = layout.get(max_tag, 0) + 1
            return layout
    
    layout = {}
    if method == "balanced":
        for tag, qty in active.items():
            layout[tag] = max(1, int((qty / total_qty) * capacity))
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=layout.get)
            if layout[max_tag] > 1: layout[max_tag] -= 1
            else: break
        while sum(layout.values()) < capacity:
            fractional = {tag: ((qty / total_qty) * capacity) - int((qty / total_qty) * capacity) for tag, qty in active.items()}
            best = max(fractional, key=fractional.get)
            layout[best] = layout.get(best, 0) + 1
    else:
        for tag, qty in active.items():
            layout[tag] = max(1, int((qty / total_qty) * capacity))
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=layout.get)
            if layout[max_tag] > 1: layout[max_tag] -= 1
            else: break
        while sum(layout.values()) < capacity:
            max_tag = max(active, key=lambda t: active[t] / (layout.get(t, 1) + 1))
            layout[max_tag] = layout.get(max_tag, 0) + 1
    return layout


# ================================================================
# ALGORITHM 1: Multi-Variation Optimizer (V4)
# ================================================================
def algo_multi_variation_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    best_score = 999999
    best_plates = None
    
    for variation in range(15):
        remaining = copy.deepcopy(demand)
        plates = []
        
        for p in range(max_plates):
            active = {k: v for k, v in remaining.items() if v > 0}
            if not active: break
            
            layout = create_valid_layout(active, capacity, "proportional")
            if not layout or sum(layout.values()) != capacity: break
            
            possible = [ceil(remaining[tag] / layout[tag]) for tag in layout if layout[tag] > 0]
            if not possible: break

            possible = sorted(possible)
            strategy_index = min(variation % len(possible), len(possible) - 1)
            sheets = max(1, possible[strategy_index])

            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * sheets))

            plates.append({"name": plate_name(len(plates) + 1), "layout": layout, "sheets": sheets, "plate_index": len(plates) + 1})

        if any(v > 0 for v in remaining.values()) and plates:
            last = plates[-1]
            for tag in remaining:
                if remaining[tag] > 0:
                    ups = max(1, last["layout"].get(tag, 1))
                    last["sheets"] += ceil(remaining[tag] / ups)
                    remaining[tag] = 0

        waste_percent = calculate_waste_percent(plates, demand)
        if waste_percent < best_score:
            best_score = waste_percent
            best_plates = plates

    return ensure_demand_met(best_plates, demand) if best_plates else None


# ================================================================
# ALGORITHM 2: AI Mutation Engine (V5)
# ================================================================
def algo_ai_mutation_optimizer(demand: dict, capacity: int, max_plates: int, iterations: int = 80) -> list:
    best_score = 999999
    best_plates = None

    for attempt in range(iterations):
        remaining = copy.deepcopy(demand)
        plates = []

        for p in range(max_plates):
            active = {k: v for k, v in remaining.items() if v > 0}
            if not active: break

            layout = create_valid_layout(active, capacity, "greedy")
            if not layout or sum(layout.values()) != capacity: break
            
            options = [ceil(remaining[tag] / layout[tag]) for tag in layout if layout[tag] > 0]
            if not options: break

            options = sorted(list(set(options)))
            sheets = max(1, random.choice(options))

            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * sheets))

            plates.append({"name": plate_name(len(plates) + 1), "layout": layout, "sheets": sheets, "plate_index": len(plates) + 1})

        if any(v > 0 for v in remaining.values()) and plates:
            last = plates[-1]
            for tag in remaining:
                if remaining[tag] > 0:
                    ups = max(1, last["layout"].get(tag, 1))
                    last["sheets"] += ceil(remaining[tag] / ups)
                    remaining[tag] = 0

        waste_percent = calculate_waste_percent(plates, demand)
        if waste_percent < best_score:
            best_score = waste_percent
            best_plates = copy.deepcopy(plates)

    return ensure_demand_met(best_plates, demand) if best_plates else None


# ================================================================
# ALGORITHM 3: AI Evolution Engine (V17)
# ================================================================
def algo_ai_evolution_optimizer(demand: dict, capacity: int, max_plates: int, generations: int = 100) -> list:
    population = []
    available_algos = [algo_ai_mutation_optimizer, algo_multi_variation_optimizer]
    
    for _ in range(20):
        candidate = random.choice(available_algos)(demand, capacity, max_plates)
        if candidate: population.append(candidate)

    if not population: return algo_multi_variation_optimizer(demand, capacity, max_plates)

    best_solution = None
    best_waste = 999999

    for generation in range(generations):
        scored = []
        for sol in population:
            if sol:
                waste = calculate_waste_percent(sol, demand)
                scored.append((waste, sol))
                if waste < best_waste:
                    best_waste = waste
                    best_solution = copy.deepcopy(sol)

        if not scored: continue
        scored.sort(key=lambda x: x[0])
        elites = [copy.deepcopy(x[1]) for x in scored[:5]]
        new_population = elites.copy()

        while len(new_population) < 20:
            parent = copy.deepcopy(random.choice(elites))
            for plate in parent:
                tags = list(plate["layout"].keys())
                if len(tags) >= 2:
                    a, b = random.sample(tags, 2)
                    if plate["layout"][a] > 1:
                        plate["layout"][a] -= 1
                        plate["layout"][b] += 1
                        if sum(plate["layout"].values()) > capacity:
                            plate["layout"][a] += 1
                            plate["layout"][b] -= 1
            new_population.append(parent)
        population = new_population

    return ensure_demand_met(best_solution, demand) if best_solution else algo_multi_variation_optimizer(demand, capacity, max_plates)


# ================================================================
# ALGORITHM 4: Smart Clustering & Dynamic Phase Chunking Engine (V6)
# ================================================================
def algo_smart_clustering_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    """V6 - High-Efficiency Multi-Phase Dynamic Chunking Engine for extreme variance"""
    if not demand: return []
    
    remaining = copy.deepcopy(demand)
    plates = []
    
    for p_idx in range(max_plates):
        active = {k: v for k, v in remaining.items() if v > 0}
        if not active: break
        
        sorted_active = sorted(active.items(), key=lambda x: x[1], reverse=True)
        total_active_qty = sum(active.values())
        
        layout = {}
        for tag, qty in sorted_active:
            share = qty / total_active_qty
            allocated_ups = int(round(share * capacity))
            if qty > 0 and allocated_ups < 1:
                allocated_ups = 0
            layout[tag] = allocated_ups
            
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=lambda k: (layout[k], remaining[k]))
            if layout[max_tag] > 0: layout[max_tag] -= 1
            else: break
            
        while sum(layout.values()) < capacity:
            max_pressure_tag = max(active.keys(), key=lambda k: remaining[k] / (layout.get(k, 0) + 1))
            layout[max_pressure_tag] = layout.get(max_pressure_tag, 0) + 1
            
        valid_sheets = []
        for tag, ups in layout.items():
            if ups > 0:
                valid_sheets.append(ceil(remaining[tag] / ups))
                
        if not valid_sheets: break
        valid_sheets.sort()
        
        target_idx = min(int(len(valid_sheets) * 0.25), len(valid_sheets) - 1)
        sheets = max(1, valid_sheets[target_idx])
        
        for tag, ups in layout.items():
            if ups > 0: remaining[tag] = max(0, remaining[tag] - (ups * sheets))
            
        plates.append({
            "name": plate_name(p_idx + 1),
            "layout": layout,
            "sheets": sheets,
            "plate_index": p_idx + 1
        })
        
    return ensure_demand_met(plates, demand)


# ================================================================
# ALGORITHM 5: Global Multi-Plate Optimizer (V2)
# ================================================================
def algo_global_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    candidates = []
    algos = [
        algo_smart_clustering_optimizer,
        algo_multi_variation_optimizer,
        algo_ai_mutation_optimizer,
        algo_ai_evolution_optimizer
    ]

    for algo in algos:
        try:
            result = algo(demand, capacity, max_plates)
            if result:
                waste = calculate_waste_percent(result, demand)
                candidates.append((waste, result))
        except:
            pass

    if not candidates: return algo_smart_clustering_optimizer(demand, capacity, max_plates)
    candidates.sort(key=lambda x: x[0])
    return ensure_demand_met(candidates[0][1], demand)


# ================================================================
# MAIN UI
# ================================================================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1: n = st.number_input("🏷️ Number of Items", 1, 500, 1)
with col2: cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 10)
with col3: maxp = st.number_input("🎨 Max Plates", 1, 50, 3)
with col4: addon = st.number_input("📈 Add-on (%)", 0.0, 50.0, 0.0, step=0.5)
with col5:
    job_number = st.text_input("🔢 Job Number", value="", placeholder="e.g., JOB-001")
    if not job_number: job_number = f"JOB-{datetime.now().strftime('%Y%m%d_%H%M')}"

st.markdown('</div>', unsafe_allow_html=True)
st.session_state['job_number'] = job_number

st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Input Method</div>', unsafe_allow_html=True)
input_mode = st.radio("Select Input Mode:", options=["✏️ Manual Input", "📂 Upload Excel File"], horizontal=True, index=1)
st.markdown('</div>', unsafe_allow_html=True)

tags, styles, colors, sizes, qty = [], [], [], [], []
original_qty, demand = {}, {}

if input_mode == "✏️ Manual Input":
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Item Quantity Details (Manual)</div>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
    col1.markdown("**SL**"); col2.markdown("**Style**"); col3.markdown("**Color**"); col4.markdown("**Size**"); col5.markdown("**Quantity**")

    for i in range(n):
        col1, col2, col3, col4, col5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        col1.markdown(f"<p style='margin-top:10px;'>{i+1}</p>", unsafe_allow_html=True)
        
        s_val = col2.text_input(f"Style", value="STYLE", key=f"s_{i}", label_visibility="collapsed")
        c_val = col3.text_input(f"Color", value="COLOR", key=f"c_{i}", label_visibility="collapsed")
        sz_val = col4.text_input(f"Size", value="FREE", key=f"sz_{i}", label_visibility="collapsed")
        q_val = col5.number_input(f"QTY", min_value=1, value=1000, key=f"q_{i}", label_visibility="collapsed")
        
        unique_tag = f"{s_val} | {c_val} | {sz_val}"
        
        styles.append(s_val)
        colors.append(c_val)
        sizes.append(sz_val)
        qty.append(q_val)
        tags.append(unique_tag)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📂 Excel/CSV File Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Excel or CSV file (Must have columns: Style, Color, Size, QTY)", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_input = pd.read_csv(uploaded_file)
            else:
                df_input = pd.read_excel(uploaded_file)
                
            df_input.columns = [str(c).strip().lower() for c in df_input.columns]
            
            col_map = {
                'style': ['style', 'style no', 'item', 'design'],
                'color': ['color', 'colour', 'shade'],
                'size': ['size', 'sz'],
                'qty': ['qty', 'quantity', 'demand', 'order qty']
            }
            
            final_cols = {}
            for target, options in col_map.items():
                for opt in options:
                    if opt in df_input.columns:
                        final_cols[target] = opt
                        break
            
            if 'qty' in final_cols:
                n = len(df_input)
                for idx, row in df_input.iterrows():
                    s_val = str(row.get(final_cols.get('style', ''), 'STYLE')).strip().upper()
                    c_val = str(row.get(final_cols.get('color', ''), 'COLOR')).strip().upper()
                    sz_val = str(row.get(final_cols.get('size', ''), 'FREE')).strip().upper()
                    q_val = int(row.get(final_cols['qty'], 0))
                    
                    if q_val > 0:
                        unique_tag = f"{s_val} | {c_val} | {sz_val}"
                        styles.append(s_val)
                        colors.append(c_val)
                        sizes.append(sz_val)
                        qty.append(q_val)
                        tags.append(unique_tag)
                st.success(f"✅ Successfully loaded {len(tags)} valid items from file!")
            else:
                st.error("❌ 'QTY' column not found in the uploaded file.")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

# Build Demand Maps
styles_dict = {}
colors_dict = {}
sizes_dict = {}

for t, s, c, sz, q in zip(tags, styles, colors, sizes, qty):
    original_qty[t] = original_qty.get(t, 0) + q
    demand[t] = ceil(original_qty[t] * (1 + addon / 100))
    styles_dict[t] = s
    colors_dict[t] = c
    sizes_dict[t] = sz

st.session_state['demand'] = demand
st.session_state['original_qty'] = original_qty


# ================================================================
# PROCESSING ENGINE & AUTO-SELECTION
# ================================================================
if tags and sum(qty) > 0:
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📊 Optimization Control Center</div>', unsafe_allow_html=True)
    
    all_results = {}
    with st.spinner("⚡ AI Engines running parallel optimization..."):
        res_v6 = algo_smart_clustering_optimizer(demand, cap, maxp)
        if res_v6: all_results["V6-Smart Clustering Optimizer"] = res_v6
        
        res_v2 = algo_global_optimizer(demand, cap, maxp)
        if res_v2: all_results["V2 - Global Multi-Plate Optimizer"] = res_v2
        
        res_v17 = algo_ai_evolution_optimizer(demand, cap, maxp)
        if res_v17: all_results["V17 - AI Evolution Engine"] = res_v17
        
        res_v5 = algo_ai_mutation_optimizer(demand, cap, maxp)
        if res_v5: all_results["V5 - AI Mutation Engine"] = res_v5
        
        res_v4 = algo_multi_variation_optimizer(demand, cap, maxp)
        if res_v4: all_results["V4 - Multi-Variation Optimizer"] = res_v4

    # Build Comparison Summary
    comp_rows = []
    for name, plates in all_results.items():
        w = calculate_waste_percent(plates, demand)
        tot_sheets = sum(p["sheets"] for p in plates)
        comp_rows.append({"Algorithm": name, "Waste %": w, "Plates": len(plates), "Total Sheets": tot_sheets})
        
    comparison_df = pd.DataFrame(comp_rows).sort_values(by="Waste %")
    best_algo_name = comparison_df.iloc[0]["Algorithm"]
    min_waste = comparison_df.iloc[0]["Waste %"]
    
    st.session_state['all_results'] = all_results

    if best_algo_name:
        st.markdown(f"""
        <div class="best-algo">
            <div class="metric-label">🏆 AUTOMATIC AI RECOMMENDATION</div>
            <div class="metric-value">{best_algo_name}</div>
            <div class="metric-label">Achieved Lowest Material Waste of <b>{min_waste}%</b></div>
        </div>
        """, unsafe_allow_html=True)

    # Main Selection Dropdown
    algo_options = list(all_results.keys())
    default_idx = algo_options.index(best_algo_name) if best_algo_name in algo_options else 0
    selected_algo = st.selectbox("🎯 Select Active Algorithm to View/Print:", options=algo_options, index=default_idx)
    
    if selected_algo:
        selected_plates = all_results[selected_algo]
        final_waste = calculate_waste_percent(selected_plates, demand)
        
        total_sheets = sum(p["sheets"] for p in selected_plates)
        grand_produced = 0
        for t in demand:
            grand_produced += sum(p["layout"].get(t, 0) * p["sheets"] for p in selected_plates)
            
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#ff4b4b;">{final_waste}%</div><div class="metric-label">📊 Material Waste</div></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(selected_plates)} / {maxp}</div><div class="metric-label">🎨 Plates Used</div></div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{total_sheets:,}</div><div class="metric-label">📄 Total Print Sheets</div></div>', unsafe_allow_html=True)
        with m_col4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{grand_produced:,}</div><div class="metric-label">📦 Total Output QTY</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("📋 Optimization Breakdown Matrix")
        summary_df = build_full_summary(selected_plates, demand, original_qty)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.subheader("🧾 Active Plate Layouts")
        p_cols = st.columns(min(len(selected_plates), 3))
        for p_idx, p in enumerate(selected_plates):
            with p_cols[p_idx % 3]:
                st.markdown(f"""
                <div class="card" style="border-top: 4px solid #667eea;">
                    <h3 style="margin:0; color:#667eea;">🎨 Plate {p['name']}</h3>
                    <p style="margin:5px 0; font-size:1.1rem;">📄 Sheets: <b>{p['sheets']:,}</b></p>
                    <p style="margin:0 0 10px 0; font-size:0.9rem; color:rgba(255,255,255,0.6);">Total UPS: {sum(p['layout'].values())} / {cap}</p>
                    <hr style="border-color:rgba(255,255,255,0.1);">
                """, unsafe_allow_html=True)
                
                for t, ups in p["layout"].items():
                    if ups > 0:
                        st.markdown(f"🔹 <span style='font-size:0.85rem;'>{t}</span> → <b>{ups} UPS</b>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
        # PDF Generator Trigger
        if REPORTLAB_AVAILABLE:
            pdf_buffer = generate_pdf_report(
                selected_plates, demand, original_qty,
                selected_algo, final_waste,
                styles_dict, colors_dict, sizes_dict, job_number
            )
            if pdf_buffer:
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Professional PDF Report",
                    data=pdf_buffer,
                    file_name=f"Plate_Report_{job_number}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("⚠️ ReportLab library missing. PDF download feature is disabled.")
            
    st.markdown('</div>', unsafe_allow_html=True)


    # ================================================================
    # 📑 VIEW INDIVIDUAL ALGORITHM REPORT SECTION
    # ================================================================
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📑 View Individual Algorithm Report</div>', unsafe_allow_html=True)
    
    report_options = list(st.session_state['all_results'].keys())
    selected_report_algo = st.selectbox("🔍 Choose Algorithm for Detailed Report:", options=report_options, key="report_algo_select")

    if selected_report_algo:
        selected_plates = st.session_state['all_results'].get(selected_report_algo)
        if selected_plates:
            st.markdown(f"### 📋 Detailed Breakdowns Matrix ({selected_report_algo})")
            full_df = build_full_summary(selected_plates, st.session_state['demand'], st.session_state['original_qty'])
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
        else:
            st.error(f"❌ Report not found for {selected_algo}")

        st.markdown("---")
        st.markdown("## 📊 Algorithm Comparison (Sorted by Waste %)")
        st.dataframe(comparison_df.style.background_gradient(cmap='viridis', subset=['Waste %']), use_container_width=True, hide_index=True)


# ================================================================
# FOOTER
# ================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
        © 2026 Plate Ratio System | Version 2 (5 Algorithms Edition)
    </p>
    <p style="color: rgba(255,255,255,0.4); font-size: 0.8rem; margin: 5px 0;">
        Optimized for Large Datasets • 5 Core Algorithms • Production Ready
    </p>
    <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.85rem; font-weight: 600; margin: 0;">
        ✨ Design & Engineered by Ovi ✨
    </p>
</div>
""", unsafe_allow_html=True)
