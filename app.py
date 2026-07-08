# app.py — PLATE RATIO SYSTEM V2 (5 Algorithms for Large Dataset)
# Optimized for Large Datasets • Production Ready
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
    .algo-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px;
    }
    .algo-badge.gold { background: #ffd700; color: #000; }
    .algo-badge.silver { background: #c0c0c0; color: #000; }
    .algo-badge.bronze { background: #cd7f32; color: #fff; }
    .algo-badge.normal { background: rgba(102,126,234,0.3); color: #fff; }
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
    <div class="version">Multi-Variation • Global • AI Evolution • AI Mutation • Base Ratio</div>
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


def ensure_demand_met(plates: list, demand: dict) -> list:
    """Adjust sheets to ensure absolutely no shortfall across any size"""
    if not plates: 
        return plates
    
    for tag in demand.keys():
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        if total_produced < demand[tag]:
            shortfall = demand[tag] - total_produced
            last_plate = plates[-1]
            ups = max(1, last_plate["layout"].get(tag, 1))
            last_plate["sheets"] += ceil(shortfall / ups)
            
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
                        styles_dict: dict, colors_dict: dict, sizes_dict: dict, 
                        job_number: str) -> BytesIO or None:
    """Generate official ReportLab PDF documentation"""
    if not REPORTLAB_AVAILABLE: 
        return None
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=14, alignment=TA_CENTER, textColor=colors.HexColor('#667eea'))
        job_style = ParagraphStyle('T2', parent=styles['Heading2'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#764ba2'))
        sub_style = ParagraphStyle('T3', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)

        story = [
            Paragraph("📊 Plate Ratio System V2 - Layout Report", title_style),
            Paragraph(f"🔢 Job Number: {job_number}", job_style),
            Paragraph(f"Engine: {algo_name} | Total Waste: {waste_percent}% | Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", sub_style),
            Spacer(1, 15)
        ]

        header = ["SL", "Style", "Color", "Size", "Original", "Target"]
        for p in plates: 
            header.append(f"Plate {p['name']}")
        header.extend(["Total Prod", "Excess", "Excess %"])
        
        table_data = [header]
        sl = 1
        for tag in demand.keys():
            row = [
                str(sl), styles_dict.get(tag, "N/A"), colors_dict.get(tag, "N/A"), sizes_dict.get(tag, "N/A"),
                str(original_qty.get(tag, 0)), str(demand[tag])
            ]
            for p in plates:
                row.append(str(p["layout"].get(tag, 0)))
                
            total_prod = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
            excess = total_prod - demand[tag]
            row.extend([str(total_prod), str(excess), f"{round((excess/demand[tag])*100,1) if demand[tag] else 0}%"])
            table_data.append(row)
            sl += 1
            
        t = Table(table_data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t)
        doc.build(story)
        buffer.seek(0)
        return buffer
    except Exception:
        return None


# ================================================================
# UNIVERSAL LAYOUT GENERATOR
# ================================================================
def create_valid_layout(active: dict, capacity: int, method: str = "balanced") -> dict:
    """Create a layout that respects capacity"""
    if not active:
        return {}
    
    total_qty = sum(active.values())
    n_items = len(active)
    
    if n_items > capacity:
        layout = {}
        if method == "balanced":
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
        
        elif method == "greedy":
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
            for tag, qty in active.items():
                ups = int((qty / total_qty) * capacity)
                if ups < 1:
                    ups = 1 if len(active) <= capacity else 0
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
    
    layout = {}
    if method == "balanced":
        for tag, qty in active.items():
            ideal = (qty / total_qty) * capacity
            base = int(ideal)
            if base < 1:
                base = 1
            layout[tag] = base
        
        while sum(layout.values()) > capacity:
            max_tag = max(layout, key=layout.get)
            if layout[max_tag] > 1:
                layout[max_tag] -= 1
            else:
                break
        
        while sum(layout.values()) < capacity:
            fractional = {}
            for tag, qty in active.items():
                ideal = (qty / total_qty) * capacity
                fractional[tag] = ideal - int(ideal)
            best = max(fractional, key=fractional.get)
            layout[best] = layout.get(best, 0) + 1
    
    else:
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


# ================================================================
# 5 ALGORITHMS FOR LARGE DATASET
# ================================================================

# ================================================================
# ALGORITHM 1: Base Ratio System (Fixed - Uses max_plates)
# ================================================================
def v1_base_ratio_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    """V1 - Base Ratio System (Now uses max_plates)"""
    total = sum(demand.values())
    if total == 0:
        return []
    
    remaining = demand.copy()
    plates = []
    
    for i in range(max_plates):
        active = {k: v for k, v in remaining.items() if v > 0}
        if not active:
            break
        
        layout = create_valid_layout(active, capacity, "balanced")
        sheets = ceil(sum(active.values()) / capacity)
        
        for tag, ups in layout.items():
            remaining[tag] = max(0, remaining[tag] - (ups * sheets))
        
        plates.append({
            "name": plate_name(i + 1),
            "layout": layout,
            "sheets": sheets,
            "plate_index": i + 1
        })
    
    if any(v > 0 for v in remaining.values()) and plates:
        last = plates[-1]
        for tag in remaining:
            if remaining[tag] > 0:
                ups = max(1, last["layout"].get(tag, 1))
                additional = ceil(remaining[tag] / ups)
                last["sheets"] += additional
                remaining[tag] = 0
    
    return ensure_demand_met(plates, demand)


# ================================================================
# ALGORITHM 2: Multi-Variation Optimizer
# ================================================================
def v4_multi_variation_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    """V4 - Multi-Variation Optimizer (Best for large datasets)"""
    best_score = 999999
    best_plates = None
    
    for variation in range(15):
        remaining = copy.deepcopy(demand)
        plates = []
        
        for p in range(max_plates):
            active = {k: v for k, v in remaining.items() if v > 0}
            if not active:
                break
            
            layout = create_valid_layout(active, capacity, "proportional")
            
            if not layout or sum(layout.values()) != capacity:
                break
            
            possible = [ceil(remaining[tag] / layout[tag]) for tag in layout if layout[tag] > 0]
            
            if not possible:
                break

            possible = sorted(possible)
            strategy_index = min(variation % len(possible), len(possible) - 1)
            sheets = max(1, possible[strategy_index])

            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * sheets))

            plates.append({
                "name": plate_name(len(plates) + 1),
                "layout": layout,
                "sheets": sheets,
                "plate_index": len(plates) + 1
            })

        if any(v > 0 for v in remaining.values()) and plates:
            last = plates[-1]
            for tag in remaining:
                if remaining[tag] > 0:
                    ups = max(1, last["layout"].get(tag, 1))
                    add_sheets = ceil(remaining[tag] / ups)
                    last["sheets"] += add_sheets
                    remaining[tag] = 0

        waste_percent = calculate_waste_percent(plates, demand)
        if waste_percent < best_score:
            best_score = waste_percent
            best_plates = plates

    return ensure_demand_met(best_plates, demand) if best_plates else v1_base_ratio_optimizer(demand, capacity, max_plates)


# ================================================================
# ALGORITHM 3: AI Mutation Engine
# ================================================================
def v5_ai_mutation_optimizer(demand: dict, capacity: int, max_plates: int, iterations: int = 80) -> list:
    """V5 - AI Mutation Engine (Random mutation for optimization)"""
    best_score = 999999
    best_plates = None

    for attempt in range(iterations):
        remaining = copy.deepcopy(demand)
        plates = []

        for p in range(max_plates):
            active = {k: v for k, v in remaining.items() if v > 0}
            if not active:
                break

            layout = create_valid_layout(active, capacity, "greedy")
            
            if not layout or sum(layout.values()) != capacity:
                break
            
            options = [ceil(remaining[tag] / layout[tag]) for tag in layout if layout[tag] > 0]

            if not options:
                break

            options = sorted(list(set(options)))
            sheets = max(1, random.choice(options))

            for tag, ups in layout.items():
                remaining[tag] = max(0, remaining[tag] - (ups * sheets))

            plates.append({
                "name": plate_name(len(plates) + 1),
                "layout": layout,
                "sheets": sheets,
                "plate_index": len(plates) + 1
            })

        if any(v > 0 for v in remaining.values()) and plates:
            last = plates[-1]
            for tag in remaining:
                if remaining[tag] > 0:
                    ups = max(1, last["layout"].get(tag, 1))
                    extra = ceil(remaining[tag] / ups)
                    last["sheets"] += extra
                    remaining[tag] = 0

        waste_percent = calculate_waste_percent(plates, demand)
        if waste_percent < best_score:
            best_score = waste_percent
            best_plates = copy.deepcopy(plates)

    return ensure_demand_met(best_plates, demand) if best_plates else v1_base_ratio_optimizer(demand, capacity, max_plates)


# ================================================================
# ALGORITHM 4: AI Evolution Engine
# ================================================================
def v17_ai_evolution_optimizer(demand: dict, capacity: int, max_plates: int, generations: int = 100) -> list:
    """V17 - AI Evolution Engine (Genetic Algorithm)"""
    population = []
    available_algos = [v1_base_ratio_optimizer, v5_ai_mutation_optimizer, v4_multi_variation_optimizer]
    
    for _ in range(20):
        candidate = random.choice(available_algos)(demand, capacity, max_plates)
        population.append(candidate)

    best_solution = None
    best_waste = 999999

    for generation in range(generations):
        scored = []

        for sol in population:
            waste = calculate_waste_percent(sol, demand)
            scored.append((waste, sol))

            if waste < best_waste:
                best_waste = waste
                best_solution = copy.deepcopy(sol)

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

    return ensure_demand_met(best_solution, demand) if best_solution else v1_base_ratio_optimizer(demand, capacity, max_plates)


# ================================================================
# ALGORITHM 5: Global Multi-Plate Optimizer
# ================================================================
def v18_global_optimizer(demand: dict, capacity: int, max_plates: int) -> list:
    """V18 - Global Multi-Plate Optimizer (Best of all)"""
    candidates = []
    algos = [
        v1_base_ratio_optimizer, 
        v4_multi_variation_optimizer, 
        v5_ai_mutation_optimizer, 
        v17_ai_evolution_optimizer
    ]

    for algo in algos:
        try:
            result = algo(demand, capacity, max_plates)
            if result:
                waste = calculate_waste_percent(result, demand)
                candidates.append((waste, result))
        except:
            pass

    if not candidates:
        return v1_base_ratio_optimizer(demand, capacity, max_plates)

    candidates.sort(key=lambda x: x[0])
    return ensure_demand_met(candidates[0][1], demand)


# ================================================================
# MAIN UI
# ================================================================

# ================== CONFIGURATION ==================
st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n = st.number_input("🏷️ Number of Items", 1, 500, 48)
with col2:
    cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 60)
with col3:
    maxp = st.number_input("🎨 Max Plates", 1, 50, 4)
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
    index=1
)

st.markdown('</div>', unsafe_allow_html=True)

# ================== INITIALIZE VARIABLES ==================
tags = []
styles = []
colors = []
sizes = []
qty = []
original_qty = {}
demand = {}

# ================== MANUAL INPUT ==================
if input_mode == "✏️ Manual Input":
    st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">📦 Item Quantity Details (Manual)</div>', unsafe_allow_html=True)
    
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
        styles.append(style_display)
        colors.append(color_display)
        sizes.append(size_display)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if any(q > 0 for q in qty):
        preview_df = pd.DataFrame({
            "SL": range(1, n + 1),
            "Style": styles,
            "Color": colors,
            "Size": sizes,
            "Quantity": qty
        })
        st.info("📋 Data Preview")
        st.dataframe(preview_df, use_container_width=True, height=200)
    
    original_qty = {tags[i]: qty[i] for i in range(len(tags)) if qty[i] > 0}
    demand = {tags[i]: ceil(qty[i] * (1 + addon / 100)) for i in range(len(tags)) if qty[i] > 0}
    
    st.session_state['item_styles'] = {tags[i]: styles[i] for i in range(len(tags))}
    st.session_state['item_colors'] = {tags[i]: colors[i] for i in range(len(tags))}
    st.session_state['item_sizes'] = {tags[i]: sizes[i] for i in range(len(tags))}

# ================== EXCEL UPLOAD ==================
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
            df = df.dropna(how='all')
            
            if df.empty:
                st.warning("⚠️ The file is empty or contains no data.")
                demand = {}
                original_qty = {}
                st.stop()
            
            columns_list = list(df.columns)
            st.success(f"✅ File loaded! Found {len(columns_list)} columns.")
            st.dataframe(df.head(5), use_container_width=True)
            
            style_col = None
            color_col = None
            size_col = None
            qty_col = None
            
            for col in columns_list:
                col_lower = str(col).lower().strip()
                if col_lower in ['style', 'styles', 'product', 'products', 'item']:
                    style_col = col
                elif col_lower in ['color', 'colors', 'colour']:
                    color_col = col
                elif col_lower in ['size', 'sizes']:
                    size_col = col
                elif col_lower in ['quantity', 'qty', 'qty.', 'quantities', 'total', 'order']:
                    qty_col = col
            
            if not style_col or not color_col or not size_col or not qty_col:
                st.info("🔍 Please select the correct columns from your Excel file:")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    style_col = st.selectbox("🎨 Style Column", columns_list, index=0)
                with c2:
                    color_col = st.selectbox("🌈 Color Column", columns_list, index=min(1, len(columns_list)-1))
                with c3:
                    size_col = st.selectbox("📏 Size Column", columns_list, index=min(2, len(columns_list)-1))
                with c4:
                    qty_col = st.selectbox("📊 Quantity Column", columns_list, index=min(3, len(columns_list)-1))
            
            excel_tags = []
            excel_styles = []
            excel_colors = []
            excel_sizes = []
            excel_qty = []
            
            for idx, row in df.iterrows():
                if row.isnull().all():
                    continue
                
                style_val = str(row.get(style_col, '')).strip() if pd.notnull(row.get(style_col)) else "N/A"
                color_val = str(row.get(color_col, '')).strip() if pd.notnull(row.get(color_col)) else "N/A"
                size_val = str(row.get(size_col, '')).strip() if pd.notnull(row.get(size_col)) else "N/A"
                
                qty_raw = row.get(qty_col, 0)
                if pd.isnull(qty_raw):
                    continue
                
                try:
                    q_val = int(float(qty_raw))
                except (ValueError, TypeError):
                    continue
                
                if q_val > 0:
                    tag = f"Item_{idx+1}_{style_val}_{size_val}"
                    excel_tags.append(tag)
                    excel_styles.append(style_val if style_val else "N/A")
                    excel_colors.append(color_val if color_val else "N/A")
                    excel_sizes.append(size_val if size_val else "N/A")
                    excel_qty.append(q_val)
            
            if excel_tags:
                st.success(f"✅ Successfully loaded {len(excel_tags)} items from Excel!")
                
                preview_df = pd.DataFrame({
                    "Style": excel_styles[:10],
                    "Color": excel_colors[:10],
                    "Size": excel_sizes[:10],
                    "Quantity": excel_qty[:10]
                })
                st.dataframe(preview_df, use_container_width=True)
                
                tags = excel_tags
                styles = excel_styles
                colors = excel_colors
                sizes = excel_sizes
                qty = excel_qty
                
                original_qty = {tags[i]: qty[i] for i in range(len(tags))}
                demand = {tags[i]: ceil(qty[i] * (1 + addon / 100)) for i in range(len(tags))}
                
                st.session_state['item_styles'] = {tags[i]: styles[i] for i in range(len(tags))}
                st.session_state['item_colors'] = {tags[i]: colors[i] for i in range(len(tags))}
                st.session_state['item_sizes'] = {tags[i]: sizes[i] for i in range(len(tags))}
                
            else:
                st.warning("⚠️ No valid data found. Please check your Excel file format.")
                demand = {}
                original_qty = {}
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            demand = {}
            original_qty = {}
    else:
        st.info("📤 Please upload an Excel file to continue.")
        demand = {}
        original_qty = {}
        st.stop()
    
    st.markdown('</div>', unsafe_allow_html=True)


# ================== CHECK DEMAND ==================
if not demand:
    st.error("⚠️ Please enter at least one item with quantity greater than 0")
    st.stop()

# ================== GENERATE BUTTON ==================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_clicked = st.button("🚀 Generate with 5 Algorithms", use_container_width=True, type="primary")

# ================== AFTER GENERATE ==================
if generate_clicked:
    if not demand:
        st.error("⚠️ Please enter at least one item with quantity greater than 0")
        st.stop()

    with st.spinner("🔍 Running 5 Algorithms for Large Dataset..."):
        
        # ================== 5 ALGORITHMS ==================
        algo_functions = {
            "V1 - Base Ratio System": lambda: v1_base_ratio_optimizer(demand, cap, maxp),
            "V4 - Multi-Variation Optimizer": lambda: v4_multi_variation_optimizer(demand, cap, maxp),
            "V5 - AI Mutation Engine": lambda: v5_ai_mutation_optimizer(demand, cap, maxp, iterations=50),
            "V17 - AI Evolution Engine": lambda: v17_ai_evolution_optimizer(demand, cap, maxp, generations=100),
            "V18 - Global Multi-Plate Optimizer": lambda: v18_global_optimizer(demand, cap, maxp),
        }
        
        # Run all algorithms with progress bar
        results = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, (algo_name, func) in enumerate(algo_functions.items()):
            status_text.text(f"Running {algo_name}... ({idx+1}/{len(algo_functions)})")
            try:
                results[algo_name] = func()
            except Exception as e:
                results[algo_name] = v1_base_ratio_optimizer(demand, cap, maxp)
            
            progress_bar.progress((idx + 1) / len(algo_functions))
        
        progress_bar.empty()
        status_text.empty()
        
        # Global fix for all algorithms
        for algo_name, plates in results.items():
            if plates:
                results[algo_name] = ensure_demand_met(plates, demand)
            else:
                results[algo_name] = v1_base_ratio_optimizer(demand, cap, maxp)
        
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
                    
                    job_number = st.session_state.get('job_number', 'JOB-00000')
                    clean_job = ''.join(c for c in job_number if c.isalnum() or c == '-')
                    excel_filename = f"{clean_job}_V2_Report.xlsx"
                    
                    st.download_button(
                        "📊 Download Excel",
                        bio_excel,
                        excel_filename,
                        use_container_width=True
                    )
                
                with col2:
                    if REPORTLAB_AVAILABLE:
                        try:
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
                                clean_job = ''.join(c for c in job_number if c.isalnum() or c == '-')
                                pdf_filename = f"Job_Number_{clean_job}_V2.pdf"
                                
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
        
        # Add badges
        def add_badges(row):
            if row["Algorithm"] == best_algo:
                return "🥇 " + row["Algorithm"]
            elif row["Algorithm"] == comparison_df.iloc[1]["Algorithm"] if len(comparison_df) > 1 else False:
                return "🥈 " + row["Algorithm"]
            elif row["Algorithm"] == comparison_df.iloc[2]["Algorithm"] if len(comparison_df) > 2 else False:
                return "🥉 " + row["Algorithm"]
            return row["Algorithm"]
        
        comparison_df_display = comparison_df.copy()
        comparison_df_display["Algorithm"] = comparison_df_display.apply(add_badges, axis=1)
        
        styled_df = comparison_df_display.style.apply(
            lambda row: ['background-color: #2e7d32; color: white'] * len(row)
            if "🥇" in row["Algorithm"] else [''] * len(row),
            axis=1
        ).format({"Waste %": "{:.2f}%"})
        
        st.dataframe(styled_df, use_container_width=True, height=400)

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

                else:
                    st.error(f"❌ Report not found for {selected_algo}")

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
    <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.85rem; font-weight: 600; margin: 10px 0 0 0;">
        ✨ Developed by Ovi | All Rights Reserved ✨
    </p>
</div>
""", unsafe_allow_html=True)
