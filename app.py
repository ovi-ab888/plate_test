# app.py — PLATE RATIO SYSTEM (V27 Only - Testing Edition)
# Inspired & Designed by Ovi's Manual Excel Workflow.

import os
import copy
from math import ceil, floor
from io import BytesIO
import streamlit as st
import pandas as pd

# ================================================================
# V27 ALGORITHM IMPLEMENTATION
# ================================================================

def algo_v27_dynamic_step_down_optimization(demand_dict, plate_capacity=60):
    """
    Algorithm V27: Dynamic Step-Down Balance Optimization (Multi-Scenario)
    
    This algorithm tests 5 different initial sheet scaling factors (80%, 90%, 100%, 110%, 120%)
    and applies a strict Step-Down logic based on the Minimum Remaining Demand 
    to completely eliminate unnecessary over-printing and minimize waste.
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
        
        # 25 Runs safety limit to prevent infinite loop
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
# STREAMLIT USER INTERFACE
# ================================================================

st.set_page_config(page_title="Ovi's Plate Ratio Optimizer (V27)", layout="wide")

st.title("📊 Plate Ratio Optimization System")
st.subheader("Algorithm V27: Dynamic Step-Down Balance Optimization (Ovi's Excel Logic)")

st.sidebar.header("Configuration")
plate_capacity = st.sidebar.number_input("Plate Capacity (Total UPS)", min_value=1, value=60, step=1)

st.sidebar.write("---")
st.sidebar.write("### Input Sizes and Demand")

# Default values based on typical user inputs
default_data = "Size_A: 15000\nSize_B: 12000\nSize_C: 7477"
input_text = st.sidebar.text_area("Enter Sizes & Quantities (Format: Size: Qty)", default_data, height=150)

# Parsing inputs
demand_dict = {}
if input_text:
    for line in input_text.strip().split('\n'):
        if ':' in line:
            parts = line.split(':')
            size_name = parts[0].strip()
            try:
                qty = int(parts[1].strip())
                if size_name and qty > 0:
                    demand_dict[size_name] = qty
            except ValueError:
                pass

if not demand_dict:
    st.warning("⚠️ Please enter valid Sizes and Quantities in the sidebar.")
else:
    st.write("### 🎯 Current Demand Summary")
    df_demand = pd.DataFrame(list(demand_dict.items()), columns=["Size/Item", "Target Demand"])
    st.dataframe(df_demand, use_container_width=True)

    if st.button("🚀 Run V27 Optimization Simulation", type="primary"):
        result = algo_v27_dynamic_step_down_optimization(demand_dict, plate_capacity)
        
        if result:
            st.success(f"✅ Optimization Completed Successfully using **Best Scenario: {result['factor_percentage']} Initial Scale**!")
            
            # Summary Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Plates Created", len(result["plates"]))
            with col2:
                st.metric("Total Waste (Over-printed)", f"{result['waste']} Pcs")
            with col3:
                st.metric("Best Initial Scenario Tried", result["factor_percentage"])
                
            # Production Breakdown Table
            st.write("### 📊 Production & Excess Breakdown")
            breakdown_data = []
            for size, target in demand_dict.items():
                produced = result["produced"].get(size, 0)
                excess = produced - target
                breakdown_data.append({
                    "Size/Item": size,
                    "Target Demand": target,
                    "Total Produced": produced,
                    "Excess (Waste)": excess if excess > 0 else 0
                })
            st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True)
            
            # Plates Layout Breakdown
            st.write("### 🛠️ Generated Plates & Grid Layout Plan")
            for plate in result["plates"]:
                with st.expander(f"📦 Plate {plate['plate_index']} — Run {plate['sheets']} Sheets", expanded=True):
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.write("**UPS Allocation (Ratio):**")
                        st.json(plate["layout"])
                    with col_p2:
                        st.write("**Production from this Plate:**")
                        st.json(plate["production"])
        else:
            st.error("❌ Optimization failed. Please check your data or plate capacity settings.")
