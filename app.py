import streamlit as st
import sys
import os

# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.ui_components import UIComponents
from utils.data_processor import get_data_processor
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Manila Water AI Foundry",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f0f8ff;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1f77b4, #2ca02c);
        color: white;
    }
    
    .Widget > label {
        color: #1f77b4;
        font-weight: bold;
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize data processor
    data_processor = get_data_processor()
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: white; margin: 0;">🌊 Manila Water</h2>
        <p style="color: #e8f4f8; margin: 0;">AI Foundry Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Choose Demo",
        ["🏠 Dashboard", "👥 HR Assistant", "🎫 Smart Ticketing", "📊 Chat with Data"],
        index=0
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🚀 POC Features
    - **AI-Powered HR Support**
    - **Intelligent Ticket Routing**
    - **Natural Language Data Queries**
    - **Real-time Analytics**
    
    ### 🔗 Integration Ready
    - SAP SuccessFactors
    - ManageEngine
    - Enterprise Lake House
    - Microsoft Teams
    """)
    
    # Route to appropriate page
    if page == "🏠 Dashboard":
        show_dashboard(data_processor)
    elif page == "👥 HR Assistant":
        show_hr_assistant()
    elif page == "🎫 Smart Ticketing":
        show_smart_ticketing()
    elif page == "📊 Chat with Data":
        show_chat_with_data()

def show_dashboard(data_processor):
    """Show main dashboard"""
    UIComponents.render_header(
        "Manila Water AI Foundry", 
        "Transforming Water Utility Operations with Artificial Intelligence",
        "🌊"
    )
    
    # Get summary statistics
    stats = data_processor.get_summary_stats()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        UIComponents.render_metric_card(
            "Population Served", 
            f"{stats['total_population_served']:,}", 
            "+2.3%",
            "👥"
        )
    
    with col2:
        UIComponents.render_metric_card(
            "Service Connections", 
            f"{stats['total_service_connections']:,}", 
            "+1.8%",
            "🏠"
        )
    
    with col3:
        UIComponents.render_metric_card(
            "Water Quality", 
            f"{stats['average_water_quality']}%", 
            "+0.2%",
            "💧"
        )
    
    with col4:
        UIComponents.render_metric_card(
            "Customer Satisfaction", 
            f"{stats['customer_satisfaction']}/5", 
            "+0.1",
            "⭐"
        )
    
    # Charts section
    st.markdown("### 📊 Performance Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Water consumption chart
        areas_data = data_processor.get_service_areas()
        if areas_data:
            fig = UIComponents.create_consumption_chart(areas_data)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Water quality gauge
        avg_quality = stats['average_water_quality']
        fig = UIComponents.create_quality_gauge(avg_quality)
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly trends
    st.markdown("### 📈 Monthly Trends")
    trends_data = data_processor.get_monthly_trends()
    if trends_data:
        fig = UIComponents.create_trends_chart(trends_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Foundry capabilities
    st.markdown("### 🤖 AI Foundry Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #1f77b4;
            text-align: center;
        ">
            <h3 style="color: #1f77b4; margin-bottom: 1rem;">👥 HR Assistant</h3>
            <p>Automate employee inquiries, leave management, and onboarding processes with conversational AI.</p>
            <ul style="text-align: left; color: #666;">
                <li>Leave request processing</li>
                <li>Policy information</li>
                <li>Benefits inquiry</li>
                <li>Onboarding guidance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff8f0, #ffe6cc);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #ff7f0e;
            text-align: center;
        ">
            <h3 style="color: #ff7f0e; margin-bottom: 1rem;">🎫 Smart Ticketing</h3>
            <p>Intelligent ticket classification, routing, and resolution with AI-powered automation.</p>
            <ul style="text-align: left; color: #666;">
                <li>Auto-categorization</li>
                <li>Smart routing</li>
                <li>Priority assignment</li>
                <li>Solution suggestions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f0fff0, #ccffcc);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #2ca02c;
            text-align: center;
        ">
            <h3 style="color: #2ca02c; margin-bottom: 1rem;">📊 Chat with Data</h3>
            <p>Natural language queries on enterprise data with real-time insights and analytics.</p>
            <ul style="text-align: left; color: #666;">
                <li>Natural language queries</li>
                <li>Real-time analytics</li>
                <li>Operational insights</li>
                <li>Ad-hoc reporting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("### 🚀 Ready to Transform Your Operations?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #1f77b4, #2ca02c);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 2rem 0;
        ">
            <h3 style="margin-bottom: 1rem; color: white;">Experience the Future of Water Utilities</h3>
            <p style="margin-bottom: 1.5rem;">Explore our AI-powered demos and see how Manila Water can revolutionize operations, improve customer satisfaction, and drive efficiency.</p>
            <p style="margin: 0; font-size: 1.1rem;"><strong>👈 Select a demo from the sidebar to get started!</strong></p>
        </div>
        """, unsafe_allow_html=True)

def show_hr_assistant():
    """Show HR Assistant page"""
    # Import here to avoid circular imports
    from pages.hr_assistant import render_hr_assistant
    render_hr_assistant()

def show_smart_ticketing():
    """Show Smart Ticketing page"""
    from pages.smart_ticketing import render_smart_ticketing
    render_smart_ticketing()

def show_chat_with_data():
    """Show Chat with Data page"""
    from pages.chat_with_data import render_chat_with_data
    render_chat_with_data()

if __name__ == "__main__":
    main()