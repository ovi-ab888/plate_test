# app.py — COMPLETE PLATE RATIO SYSTEM (V27 SHEET-DRIVEN SPECIAL EDITION)
# Design by Ovi • Max Plates Enforced & Candidate Sheets Driven Optimization

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
    page_title="Plate Ratio System - V27 Sheet Edition",
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
    #MainMenu, header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================================================================
# HELPER FUNCTIONS
# ================================================================
def plate_name(n: int) -> str:
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
    total_produced = 0
    total_demand = sum(demand.values())
    if total_demand == 0: return 0.0

    for tag in demand:
        produced_qty = 0
        for p in plates:
            if p and "layout" in p:
                produced_qty += p["layout"].get(tag, 0) * p.get("sheets", 0)
        total_produced += produced_qty

    if total_produced == 0: return 100.0
    waste = total_produced - total_demand
    return round(max(0, (waste / total_produced) * 100), 2)

def ensure_demand_met(plates: list, demand: dict) -> list:
    if not plates: return plates
    for tag in demand.keys():
        total_produced = sum(p["layout"].get(tag, 0) * p["sheets"] for p in plates)
        if total_produced < demand[tag]:
            shortfall = demand[tag] - total_produced
            last_plate = plates[-1]
            ups = max(1, last_plate["layout"].get(tag, 1))
            last_plate["sheets"] += ceil(shortfall / ups)
            
    for p in plates:
        p["production"] = {tag: ups * p["sheets"] for tag, ups in p["layout"].items()}
    return plates

def build_full_summary(plates: list, demand: dict, original_qty: dict) -> pd.DataFrame:
    rows = []
    sl = 1
    for tag in demand.keys():
        row = {"SL": sl, "Tag": tag, "Original QTY": original_qty.get(tag, 0), "Produced (+Add-on)": demand[tag]}
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
    total_row = {"SL": "📊", "Tag": "TOTAL", "Original QTY": df["Original QTY"].sum(), "Produced (+Add-on)": df["Produced (+Add-on)"].sum()}
    for p in plates:
        total_row[f"Plate {p['name']}"] = df[f"Plate {p['name']}"].sum()
    total_row["Total Produced QTY"] = df["Total Produced QTY"].sum()
    total_row["Excess"] = df["Excess"].sum()
    total_row["Excess %"] = f"{round((df['Excess'].sum() / total_row['Total Produced QTY']) * 100, 2) if total_row['Total Produced QTY'] else 0}%"
    
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

# ================================================================
# NEW EXPERT V27: CANDIDATE SHEET-DRIVEN SIMULATION (💡 FIXED)
# ================================================================
def algo_v27_candidate_sheet_optimization(demand_dict, plate_capacity=60, max_plates=3):
    TOTAL_UPS = plate_capacity
    total_initial_demand = sum(demand_dict.values())
    if total_initial_demand == 0: return None
    
    # ১. বেসলাইন শিট ক্যালকুলেশন
    estimated_base_sheets = total_initial_demand / TOTAL_UPS
    
    # ২. ডাইনামিক ক্যান্ডিডেট শিট জেনারেশন (ব্যবধানে রাউন্ড শিট তৈরি)
    start_sheet = max(50, int(estimated_base_sheets * 0.5))
    end_sheet = int(estimated_base_sheets * 1.6)
    step = 50 if estimated_base_sheets > 500 else 25
    
    candidate_sheets = list(range(start_sheet, end_sheet, step))
    if int(estimated_base_sheets) not in candidate_sheets:
        candidate_sheets.append(int(estimated_base_sheets))
    candidate_sheets = sorted([c for c in candidate_sheets if c > 0])

    best_result = None
    min_total_waste = float('inf')
    
    # ৩. ক্যান্ডিডেট শিট ধরে সিমুলেশন লুপ
    for candidate in candidate_sheets:
        current_demand = copy.deepcopy(demand_dict)
        plates_list = []
        run_count = 1
        is_first_run = True
        
        while sum(current_demand.values()) > 0 and run_count <= max_plates:
            active_sizes = {k: v for k, v in current_demand.items() if v > 0}
            if not active_sizes: break
            
            allocated_ups = {}
            total_active_demand = sum(active_sizes.values())
            
            # শেষ প্লেট হলে সব অবশিষ্টাংশ রেশিও অনুযায়ী বণ্টন
            if run_count == max_plates:
                if len(active_sizes) <= TOTAL_UPS:
                    for size in active_sizes: allocated_ups[size] = 1
                    remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                    if remaining_ups > 0:
                        for size, _ in sorted(active_sizes.items(), key=lambda x: x[1], reverse=True):
                            if remaining_ups == 0: break
                            allocated_ups[size] += 1
                            remaining_ups -= 1
                else:
                    allocated_ups = {sz: int(floor((qty / total_active_demand) * TOTAL_UPS)) for sz, qty in active_sizes.items()}
                    remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                    for size, _ in sorted(active_sizes.items(), key=lambda x: (x[1]/total_active_demand * TOTAL_UPS) - floor((x[1]/total_active_demand) * TOTAL_UPS), reverse=True):
                        if remaining_ups == 0: break
                        allocated_ups[size] += 1
                        remaining_ups -= 1
            else:
                # সাধারণ প্লেটের জন্য প্রো-রেটা ডিস্ট্রিবিউশন
                raw_ups = {sz: (qty / total_active_demand) * TOTAL_UPS for sz, qty in active_sizes.items()}
                allocated_ups = {sz: max(1, int(floor(val))) for sz, val in raw_ups.items()}
                remaining_ups = TOTAL_UPS - sum(allocated_ups.values())
                if remaining_ups > 0:
                    for size, _ in sorted(raw_ups.items(), key=lambda x: x[1] - allocated_ups[x[0]], reverse=True):
                        if remaining_ups == 0: break
                        allocated_ups[size] += 1
                        remaining_ups -= 1
                while sum(allocated_ups.values()) > TOTAL_UPS:
                    max_tag = max(allocated_ups, key=allocated_ups.get)
                    allocated_ups[max_tag] -= 1

            # প্রথম প্লেটে ক্যান্ডিডেট শিট অ্যাপ্লাই হবে
            if is_first_run:
                run_sheets = candidate
                is_first_run = False
                if run_count == max_plates:
                    needed = [ceil(current_demand[sz] / max(1, allocated_ups.get(sz, 1))) for sz in active_sizes]
                    if needed: run_sheets = max(run_sheets, max(needed))
            else:
                if run_count == max_plates:
                    needed = [ceil(current_demand[sz] / max(1, allocated_ups.get(sz, 1))) for sz in active_sizes]
                    run_sheets = max(needed) if needed else 1
                else:
                    run_sheets = max(1, min(ceil(qty / allocated_ups.get(sz, 1)) for sz, qty in active_sizes.items()))
            
            plate_production = {sz: ups * run_sheets for sz, ups in allocated_ups.items()}
            for sz, qty in plate_production.items():
                current_demand[sz] = max(0, current_demand[sz] - qty)
            
            plates_list.append({
                "plate_index": run_count, "name": plate_name(run_count),
                "layout": allocated_ups, "sheets": run_sheets, "production": plate_production
            })
            run_count += 1
            
        # ওয়েস্টেজ ক্যালকুলেশন করে সেরা স্কোর খোঁজা
        total_produced = {sz: 0 for sz in demand_dict.keys()}
        for p in plates_list:
            for sz, qty in p["production"].items(): total_produced[sz] += qty
        
        scenario_waste = sum(max(0, total_produced[sz] - target) for sz, target in demand_dict.items())
        
        if scenario_waste < min_total_waste:
            min_total_waste = scenario_waste
            best_result = {"plates": plates_list, "waste": scenario_waste, "candidate_sheet": run_sheets}
            
    return best_result

# ================================================================
# STREAMLIT UI & INTERFACE
# ================================================================
st.markdown('<div class="main-header"><h1>📊 Plate Ratio Intelligence System</h1><p>V27 Candidate-Sheet Driven Edition</p><div class="designer-name">✨ Design by Ovi ✨</div></div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title" style="text-align: center; display: block; width: 100%;">⚙️ Production Configuration</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
with col1: n = st.number_input("🏷️ Number of Items", 1, 500, 3)
with col2: cap = st.number_input("📀 Plate Capacity (UPS)", 1, 200, 60)
with col3: maxp = st.number_input("🎨 Max Plates", 1, 50, 3)
with col4: addon = st.number_input("📈 Add-on (%)", 0.0, 50.0, 0.0, step=0.5)
with col5: job_number = st.text_input("🔢 Job Number", value="JOB-001")

st.markdown('</div>', unsafe_allow_html=True)

# Input Mode Selection
input_mode = st.radio("Select Input Mode:", options=["✏️ Manual Input", "📂 Upload Excel File"], horizontal=True)

styles_dict, colors_dict, sizes_dict, original_qty, demand_dict = {}, {}, {}, {}, {}
tags = []

if input_mode == "✏️ Manual Input":
    for i in range(n):
        c1, c2, c3, c4, c5 = st.columns([0.5, 1.5, 1.5, 1.5, 2])
        with col1: st.write(f"{i+1}")
        style_val = c2.text_input("Style", value=f"Style_{i+1}", key=f"s_{i}")
        color_val = c3.text_input("Color", value="Black", key=f"c_{i}")
        size_val = c4.text_input("Size", value=chr(83 + i % 4), key=f"z_{i}")
        qty_val = c5.number_input("Quantity", min_value=0, value=1000 * (i+1), step=100, key=f"q_{i}")
        
        tag = f"Item_{i+1}_{style_val}_{size_val}"
        tags.append(tag)
        styles_dict[tag], colors_dict[tag], sizes_dict[tag], original_qty[tag] = style_val, color_val, size_val, qty_val
        demand_dict[tag] = int(qty_val * (1 + addon / 100))
else:
    uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])
    if uploaded_file:
        df_xl = pd.read_excel(uploaded_file, skiprows=29)
        st.dataframe(df_xl.head(), use_container_width=True)
        columns_list = list(df_xl.columns)
        
        c_1, c_2, c_3, c_4 = st.columns(4)
        style_col = c_1.selectbox("Style Column", columns_list)
        color_col = c_2.selectbox("Color Column", columns_list)
        size_col = c_3.selectbox("Size Column", columns_list)
        qty_col = c_4.selectbox("Quantity Column", columns_list)
        
        for index, row in df_xl.iterrows():
            st_val, cl_val, sz_val = str(row.get(style_col, 'N/A')), str(row.get(color_col, 'N/A')), str(row.get(size_col, 'N/A'))
            q_val = int(row[qty_col]) if pd.notnull(row.get(qty_col)) else 0
            tag = f"Item_{index+1}_{st_val}_{sz_val}"
            tags.append(tag)
            styles_dict[tag], colors_dict[tag], sizes_dict[tag], original_qty[tag] = st_val, cl_val, sz_val, q_val
            demand_dict[tag] = int(q_val * (1 + addon / 100))

# ================================================================
# EXECUTION
# ================================================================
if tags and st.button("🚀 Calculate V27 Candidate-Sheet Ratios", type="primary"):
    res = algo_v27_candidate_sheet_optimization(demand_dict, cap, int(maxp))
    if res:
        final_plates = ensure_demand_met(res["plates"], demand_dict)
        w_percent = calculate_waste_percent(final_plates, demand_dict)
        
        st.markdown(f'<div class="best-algo">🎖️ Best Candidate Print Sheet Selection: {res["candidate_sheet"]} Sheets </div>', unsafe_allow_html=True)
        
        cm1, cm2, cm3 = st.columns(3)
        cm1.markdown(f'<div class="metric-card"><div class="metric-value">{len(final_plates)}</div><div class="metric-label">Plates Bounded</div></div>', unsafe_allow_html=True)
        cm2.markdown(f'<div class="metric-card"><div class="metric-value">{w_percent}%</div><div class="metric-label">Material Waste</div></div>', unsafe_allow_html=True)
        cm3.markdown(f'<div class="metric-card"><div class="metric-value">{sum(p["sheets"] for p in final_plates)}</div><div class="metric-label">Total Print Sheets</div></div>', unsafe_allow_html=True)
        
        st.write("##")
        df_summary = build_full_summary(final_plates, demand_dict, original_qty)
        df_summary['Tag'] = df_summary['Tag'].apply(lambda x: styles_dict.get(x, x) if x != "TOTAL" else "TOTAL")
        st.dataframe(df_summary, use_container_width=True)

# ================== RESULTS DISPLAY ==================
if st.session_state.get('calculated', False):
    plates = st.session_state['v27_plates']
    w_percent = st.session_state['v27_waste']
    factor = st.session_state['v27_factor']
    
    # 🌟 Performance Summary Cards
    st.markdown(f"""
    <div class="best-algo">
        🎖️ Best Simulation Strategy Found: <strong>{factor}</strong> Scaling 
        <span style="margin-left: 20px; font-size: 0.9rem;">
            | Waste: {w_percent}%
        </span>
    </div>
    """, unsafe_allow_html=True)
    
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
    df_summary = build_full_summary(plates, st.session_state['demand_dict'], st.session_state['original_qty'])
    
    # Replace Technical internal tags with beautiful style labels for presentation
    if not df_summary.empty:
        styles_dict_local = st.session_state.get('styles_dict', {})
        df_summary['Tag'] = df_summary['Tag'].apply(lambda x: styles_dict_local.get(x, x) if x != "TOTAL" else "TOTAL")
    
    st.dataframe(df_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Plate Layout Breakdowns
    st.markdown('<div class="card"><div class="card-title">🛠️ Individual Plate Matrix Detail</div>', unsafe_allow_html=True)
    sizes_dict_local = st.session_state.get('sizes_dict', {})
    for p in plates:
        with st.expander(f"📦 Plate {p['name']} — Print Run: {p['sheets']} Sheets", expanded=True):
            p_cols = st.columns(2)
            with p_cols[0]:
                st.write("**Ratio Layout (UPS Allocation per Size):**")
                display_layout = {sizes_dict_local.get(k, k): v for k, v in p["layout"].items() if v > 0}
                st.json(display_layout)
            with p_cols[1]:
                st.write("**Total Output Pieces from this Plate:**")
                display_prod = {sizes_dict_local.get(k, k): v for k, v in p["production"].items() if v > 0}
                st.json(display_prod)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download Section
    st.markdown('<div class="card"><div class="card-title">📥 Download Reports</div>', unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        # Excel Download
        bio_excel = BytesIO()
        with pd.ExcelWriter(bio_excel, engine="openpyxl") as writer:
            df_summary.to_excel(writer, sheet_name="Summary", index=False)
            
            # Plate details
            plate_rows = []
            for p in plates:
                plate_rows.append({
                    "Plate ID": p["name"],
                    "Sheets": p["sheets"],
                    "Total UPS": sum(p["layout"].values()),
                    "Layout": str(p["layout"])
                })
            pd.DataFrame(plate_rows).to_excel(writer, sheet_name="Plate Details", index=False)
        
        bio_excel.seek(0)
        st.download_button(
            "📊 Download Excel Report",
            bio_excel,
            f"{job_number}_V27_Report.xlsx",
            use_container_width=True
        )
    
    with col_d2:
        # PDF Download
        if REPORTLAB_AVAILABLE:
            pdf_buffer = generate_pdf_report(
                plates, 
                st.session_state['demand_dict'], 
                st.session_state['original_qty'], 
                "Algorithm V27 (Step-Down)", 
                w_percent, 
                st.session_state.get('styles_dict', {}),
                st.session_state.get('colors_dict', {}),
                st.session_state.get('sizes_dict', {}),
                job_number
            )
            
            if pdf_buffer:
                st.download_button(
                    "📄 Download PDF Report",
                    pdf_buffer,
                    f"{job_number}_V27_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("ℹ️ PDF download requires reportlab. Install with: pip install reportlab")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================================================================
# FOOTER
# ================================================================
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid rgba(102,126,234,0.3); background: rgba(255,255,255,0.02); border-radius: 20px;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.85rem; margin: 0;">
        © 2026 Plate Ratio System | Version 27 (Testing Edition)
    </p>
    <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 8px 0;">
        Enterprise Production Optimization Framework • Manual Logic Injected • Production Ready
    </p>
    <p style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 0.85rem; font-weight: 600; margin: 10px 0 0 0;">
        ✨ Developed by Ovi | All Rights Reserved ✨
    </p>
</div>
""", unsafe_allow_html=True)
