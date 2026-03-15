import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from ai_risk_engine.data_tracker import get_dashboard_stats, get_device_stats

# Page config
st.set_page_config(
    page_title="SentinelAI Admin Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

# Force data refresh on each run
import importlib
import ai_risk_engine.data_tracker as tracker_module
importlib.reload(tracker_module)
from ai_risk_engine.data_tracker import get_dashboard_stats

# Get data (freshly loaded)
stats = get_dashboard_stats()

# ============= HEADER =============
st.title("🛡️ Admin DashBoard")

# ============= KPI CARDS =============
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total AI Prompts",
        value=stats["total"],
        delta="↑ 24 this week"
    )

with col2:
    st.metric(
        label="Safe Prompts",
        value=stats["safe"],
        delta=f"{round(stats['safe']/stats['total']*100)}% of total",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Sanitized Prompts",
        value=stats["sanitized"],
        delta=f"{round(stats['sanitized']/stats['total']*100)}% of total",
        delta_color="normal"
    )

with col4:
    st.metric(
        label="Blocked Prompts",
        value=stats["blocked"],
        delta=f"{round(stats['blocked']/stats['total']*100)}% of total",
        delta_color="off"
    )

st.divider()

# ============= CHARTS SECTION =============
chart_col1, chart_col2, chart_col3 = st.columns(3)

# Chart 1: Risk Distribution (Pie)
with chart_col1:
    st.subheader("Prompt Risk Distribution")
    
    risk_data = stats["risk_distribution"]
    colors = ["#00dc82", "#ffb340", "#ff4d4d"]
    
    fig_risk = go.Figure(data=[go.Pie(
        labels=list(risk_data.keys()),
        values=list(risk_data.values()),
        marker=dict(colors=colors),
        textinfo="label+percent",
    )])
    fig_risk.update_layout(
        height=350,
        showlegend=True,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(fig_risk, use_container_width=True)

# Chart 2: Prompt Type Distribution (Bar)
with chart_col2:
    st.subheader("Prompt Type Distribution")
    
    prompt_types = stats["prompt_types"]
    colors_types = ["#4f46e5", "#7c3aed", "#06b6d4", "#ec4899"]
    
    fig_types = go.Figure(data=[go.Bar(
        y=list(prompt_types.keys()),
        x=list(prompt_types.values()),
        orientation='h',
        marker=dict(color=colors_types[:len(prompt_types)])
    )])
    fig_types.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(color="white"),
        yaxis=dict(color="white")
    )
    st.plotly_chart(fig_types, use_container_width=True)

# Chart 3: Security Actions (Bar)
with chart_col3:
    st.subheader("Security Actions")
    
    actions_data = {
        "Allow": stats["safe"],
        "Sanitize": stats["sanitized"],
        "Block": stats["blocked"]
    }
    colors_actions = ["#00dc82", "#ffb340", "#ff4d4d"]
    
    fig_actions = go.Figure(data=[go.Bar(
        x=list(actions_data.keys()),
        y=list(actions_data.values()),
        marker=dict(color=colors_actions)
    )])
    fig_actions.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(color="white"),
        yaxis=dict(color="white")
    )
    st.plotly_chart(fig_actions, use_container_width=True)

st.divider()

# ============= EMPLOYEE ACTIVITY FEED =============
st.subheader("Employee Activity Feed")

# Prepare device data
device_data = []
for device_id, device_info in stats["devices"].items():
    record = {
        "EMPLOYEE DEVICE": device_id,
        "PROMPTS": device_info["prompts"],
        "HIGH RISK": device_info["high_risk"],
        "ACTIONS TAKEN": f"{'✓ Allowed: ' + str(device_info['actions'].get('Allowed', 0)) if device_info['actions'].get('Allowed', 0) > 0 else ''} "
                         f"{'⚠ Sanitized: ' + str(device_info['actions'].get('Sanitized', 0)) if device_info['actions'].get('Sanitized', 0) > 0 else ''} "
                         f"{'✗ Blocked: ' + str(device_info['actions'].get('Blocked', 0)) if device_info['actions'].get('Blocked', 0) > 0 else ''}".strip()
    }
    device_data.append(record)

if device_data:
    # Display as styled dataframe
    df_devices = pd.DataFrame(device_data)
    
    # Use Streamlit's native dataframe renderer with custom styling
    st.dataframe(
        df_devices,
        use_container_width=True,
        hide_index=True,
        column_config={
            "EMPLOYEE DEVICE": st.column_config.TextColumn("EMPLOYEE DEVICE", width="medium"),
            "PROMPTS": st.column_config.NumberColumn("PROMPTS", width="small"),
            "HIGH RISK": st.column_config.NumberColumn("HIGH RISK", width="small"),
            "ACTIONS TAKEN": st.column_config.TextColumn("ACTIONS TAKEN", width="large"),
        }
    )
else:
    st.info("No device activity recorded yet")

st.divider()

# ============= SIDEBAR: DETAILED ANALYTICS =============
with st.sidebar:
    st.title("📊 Analytics")
    
    selected_device = st.selectbox(
        "Select Device for Detailed View",
        [device for device in stats["devices"].keys()],
        label_visibility="collapsed"
    )
    
    if selected_device:
        device_stats = stats["devices"][selected_device]
        
        st.subheader(f"📱 {selected_device}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Prompts", device_stats["prompts"])
        with col2:
            st.metric("High Risk", device_stats["high_risk"], delta_color="off")
        
        # Action breakdown
        st.subheader("Action Breakdown")
        actions = device_stats["actions"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✓ Allowed", actions.get("Allowed", 0), label_visibility="collapsed")
        with col2:
            st.metric("⚠ Sanitized", actions.get("Sanitized", 0), label_visibility="collapsed")
        with col3:
            st.metric("✗ Blocked", actions.get("Blocked", 0), label_visibility="collapsed")
        
        # Prompt type breakdown for device
        st.subheader("Prompt Breakdown")
        device_analytics = get_device_stats(selected_device)
        if device_analytics["prompt_types"]:
            prompt_df = pd.DataFrame(
                list(device_analytics["prompt_types"].items()),
                columns=["Type", "Count"]
            )
            st.bar_chart(prompt_df.set_index("Type"), use_container_width=True)
        
    # System info
    st.divider()
    st.subheader("ℹ️ System Info")
    st.text(f"Dashboard Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
