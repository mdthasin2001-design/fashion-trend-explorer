import streamlit as st
import pandas as pd
import plotly.graph_objects as dict_to_graph
import time
import random

# Page configuration
st.set_page_config(page_title="Fashion Trend Explorer", page_icon="👕", layout="centered")

# App Title
st.title("Fashion Trend Explorer")
st.markdown("---")

# --- SIDEBAR / CONTROLS ---
st.subheader("📊 Trend Search Controls")
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    brand = st.selectbox("Select Brand", ["All Brands", "Tommy Hilfiger", "Calvin Klein", "H&M", "Zara", "Levi's", "Kontoor", "Marks & Spencer", "Uniqlo"])
with col2:
    demographic = st.selectbox("Demographic", ["Women", "Men", "Kids"])
with col3:
    season = st.selectbox("Season", ["Summer", "Winter", "Autumn", "Spring"])
with col4:
    apparel_type = st.selectbox("Apparel Type", ["Top", "Bottom", "Outerwear", "Dress", "Jeans"])

# --- TEXTILE SPECS GENERATOR ENGINE ---
def get_textile_specs(season_input, apparel_input):
    specs = {
        "Primary Material": "100% Cotton",
        "Color Palette": "Neutrals",
        "Fabric Weight": "180 GSM",
        "Target Silhouette": "Regular Fit"
    }
    
    if season_input == "Summer":
        specs["Primary Material"] = "Linen Blends / Lightweight Poplin" if apparel_input != "Jeans" else "10-11 oz Lightweight Denim"
        specs["Color Palette"] = "Vibrant Pastels & Crisp Whites"
        specs["Fabric Weight"] = "110 - 140 GSM"
        specs["Target Silhouette"] = "Relaxed / Fluid Fit"
    elif season_input == "Winter":
        specs["Primary Material"] = "Heavyweight Twill / Wool Blends / Fleece" if apparel_input != "Jeans" else "13.5 - 15 oz Rigid Denim"
        specs["Color Palette"] = "Deep Earth Tones & Dark Neutrals"
        specs["Fabric Weight"] = "320 - 450 GSM"
        specs["Target Silhouette"] = "Oversized / Structured Layering"
    elif season_input == "Autumn":
        specs["Primary Material"] = "Corduroy / Heavy Knits / Canvas"
        specs["Color Palette"] = "Warm Neutrals, Ochre & Burgundy"
        specs["Fabric Weight"] = "220 - 280 GSM"
        specs["Target Silhouette"] = "Boxy / Regular Fit"
    elif season_input == "Spring":
        specs["Primary Material"] = "Tencel Blends / Fine Jersey / Chambray"
        specs["Color Palette"] = "Soft Pastels & Bright Accents"
        specs["Fabric Weight"] = "140 - 180 GSM"
        specs["Target Silhouette"] = "Tailored / Slouchy Balance"
        
    return specs

# --- GENERATE SELECTION-BASED DATA ENGINE ---
def generate_simulated_trends(b, d, s, a):
    # Create a seed based on text inputs so the same selection always yields the same realistic data
    seed_value = len(b) + len(d) + len(s) + len(a)
    random.seed(seed_value)
    
    # Generate interactive, unique growth scores dynamically
    base_growth = random.randint(35, 145)
    
    trend_data = {
        "Status": ["🔥 Breakthrough", "☑️ Rising", "☑️ Rising", "☑️ Rising"],
        "Item Name / Detail": [
            f"{b} Sustainable {s} {a}" if b != "All Brands" else f"Eco-Friendly {s} {a}",
            f"D5 Waterless Dyed {s} Custom Blend",
            f"Recycled Denim Core {a} Pipeline",
            f"Zero-Waste Circular {d}'s Pattern"
        ],
        "YoY Growth": [f"+{base_growth}%", f"+{int(base_growth*0.7)}%", f"+{int(base_growth*0.4)}%", f"+{int(base_growth*0.3)}%"]
    }
    
    # Calculate a custom velocity score out of 100
    calculated_velocity = min(max(int(base_growth * 0.8), 55), 98)
    
    return pd.DataFrame(trend_data), calculated_velocity

# --- RUN ANALYSIS ---
if st.button("Analyze Real-Time Trends", type="primary", use_container_width=True):
    with st.spinner("Analyzing target consumer streams and textile data..."):
        time.sleep(1.2) # Adds a realistic loading feel
        simulated_df, trend_score = generate_simulated_trends(brand, demographic, season, apparel_type)
    
    # 1. VISUAL CHART: Dynamic Trend Score
    st.markdown("### Trend Velocity Index")
    baseline_score = 65
    
    fig = dict_to_graph.Figure()
    fig.add_trace(dict_to_graph.Bar(
        y=['Current Trend', 'Category Baseline'],
        x=[trend_score, baseline_score],
        orientation='h',
        marker=dict(color=['#3b82f6', '#475569']),
        text=[f"{trend_score} pts", f"{baseline_score} pts"],
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(color='white', size=14)
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0, 100], showgrid=True, gridcolor='#334155'),
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=200,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. MARKET MICRO-TRENDS TABLE
    st.markdown("### Live Market Micro-Trends")
    st.table(simulated_df)

    # 3. TECHNICAL SPECIFICATIONS TABLE
    st.markdown("### Technical Product Specifications")
    tech_specs = get_textile_specs(season, apparel_type)
    
    specs_df = pd.DataFrame({
        "Attribute": list(tech_specs.keys()),
        "Technical Spec": list(tech_specs.values())
    })
    st.table(specs_df)
