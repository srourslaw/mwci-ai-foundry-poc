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

# Custom CSS for professional styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f0f8ff;
        border: 1px solid #1f77b4;
        border-radius: 8px;
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
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2, #667eea);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar styling improvements */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Main content area */
    .css-18e3th9 {
        padding-top: 1rem;
    }
    
    /* Header improvements */
    h1, h2, h3 {
        color: #667eea;
    }
    
    /* Update metric card border colors */
    .metric-card {
        border-left-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize data processor
    data_processor = get_data_processor()
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Executive Dashboard"
    
    # Always show sidebar with ONLY navigation
    st.sidebar.markdown("""
    <div style="
        text-align: center; 
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        margin-bottom: 1rem;
    ">
        <h2 style="color: white; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🌊 Manila Water</h2>
        <p style="color: white; margin: 0; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">AI Foundry Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons only - nothing else
    nav_options = [
        "🏠 Executive Dashboard", 
        "👥 HR AI Assistant", 
        "🎫 Smart Ticketing System", 
        "📊 Chat With Data Analytics"
    ]
    
    for option in nav_options:
        if st.sidebar.button(option, use_container_width=True, key=f"nav_{option}"):
            st.session_state.current_page = option
            st.rerun()
    
    # API Configuration Section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 AI Configuration")
    
    # API Key inputs
    with st.sidebar.expander("🤖 Configure AI Services", expanded=False):
        st.markdown("**Add your API keys for AI features:**")
        
        gemini_key = st.text_input(
            "🔹 Gemini API Key", 
            type="password", 
            help="For AI responses and ticket classification",
            key="gemini_api_input"
        )
        
        openai_key = st.text_input(
            "🔹 OpenAI API Key (Optional)", 
            type="password", 
            help="Fallback AI service",
            key="openai_api_input"
        )
        
        anthropic_key = st.text_input(
            "🔹 Anthropic API Key (Optional)", 
            type="password", 
            help="For advanced data analysis",
            key="anthropic_api_input"
        )
        
        # Save button
        if st.button("💾 Save API Keys", use_container_width=True):
            if gemini_key:
                st.session_state.gemini_api_key = gemini_key
                st.success("✅ Gemini API key saved!")
            if openai_key:
                st.session_state.openai_api_key = openai_key
                st.success("✅ OpenAI API key saved!")
            if anthropic_key:
                st.session_state.anthropic_api_key = anthropic_key
                st.success("✅ Anthropic API key saved!")
            st.rerun()
        
        # Test API key button
        if st.session_state.get('gemini_api_key'):
            if st.button("🧪 Test Gemini API", use_container_width=True):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=st.session_state.gemini_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content("Say 'Hello from Manila Water!'")
                    st.success(f"✅ API Test Success: {response.text}")
                except Exception as e:
                    st.error(f"❌ API Test Failed: {str(e)}")
                    if "API_KEY_INVALID" in str(e):
                        st.error("🔑 Your API key appears to be invalid")
                    elif "quota" in str(e).lower():
                        st.error("📊 API quota exceeded")
                    else:
                        st.error("🔧 Check your API key format")
        
        # Status indicators with real-time validation
        st.markdown("**AI Service Status:**")
        
        # Test AI manager to see actual status
        from utils.ai_models import get_ai_manager
        ai_manager = get_ai_manager()
        
        gemini_working = bool(ai_manager.gemini_model)
        openai_working = bool(ai_manager.openai_client)
        anthropic_working = bool(ai_manager.anthropic_client)
        
        gemini_status = "🟢 Ready" if gemini_working else "🔴 Not configured"
        openai_status = "🟢 Ready" if openai_working else "⚪ Optional"
        anthropic_status = "🟢 Ready" if anthropic_working else "⚪ Optional"
        
        st.markdown(f"**Gemini:** {gemini_status}")
        st.markdown(f"**OpenAI:** {openai_status}")  
        st.markdown(f"**Claude:** {anthropic_status}")
        
        # Debug info
        if hasattr(ai_manager, 'available_keys'):
            if any(ai_manager.available_keys.values()) and not any([gemini_working, openai_working, anthropic_working]):
                st.error("⚠️ API keys detected but not working. Check key format!")
        
        if not gemini_working and not openai_working and not anthropic_working:
            if st.session_state.get('gemini_api_key'):
                st.warning("🔄 Try refreshing the page after adding keys")
            else:
                st.info("💡 Add your Gemini API key to enable AI features!")
    
    page = st.session_state.current_page
    
    # Route to appropriate page
    if page == "🏠 Executive Dashboard":
        show_dashboard(data_processor)
    elif page == "👥 HR AI Assistant":
        show_hr_assistant()
    elif page == "🎫 Smart Ticketing System":
        show_smart_ticketing()
    elif page == "📊 Chat With Data Analytics":
        show_chat_with_data()

def show_dashboard(data_processor):
    """Show comprehensive enterprise dashboard"""
    
    # Header with executive branding
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🌊 Manila Water AI Foundry</h1>
        <h3 style="margin: 0.5rem 0 0 0; font-weight: 300; opacity: 0.9;">Enterprise Command Center & AI Operations Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # API Configuration Notice
    if not st.session_state.get('gemini_api_key'):
        st.info("💡 **Enable AI Features:** Add your API keys in the sidebar under '🤖 Configure AI Services' to unlock HR assistance, smart ticketing, and data analytics!")
    
    # Get all data for comprehensive view
    stats = data_processor.get_summary_stats()
    areas_data = data_processor.get_service_areas()
    trends_data = data_processor.get_monthly_trends()
    
    # Executive KPI Dashboard
    st.markdown("## 📊 Executive KPIs & Performance Metrics")
    
    # Main metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 5px solid #667eea;
            text-align: center;
        ">
            <h4 style="color: #666; margin: 0; font-size: 0.9rem;">POPULATION SERVED</h4>
            <h2 style="color: #667eea; margin: 0.5rem 0; font-weight: 700;">{stats['total_population_served']:,}</h2>
            <p style="color: #28a745; margin: 0; font-size: 0.8rem;">+2.3% ▲</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 5px solid #764ba2;
            text-align: center;
        ">
            <h4 style="color: #666; margin: 0; font-size: 0.9rem;">SERVICE CONNECTIONS</h4>
            <h2 style="color: #764ba2; margin: 0.5rem 0; font-weight: 700;">{stats['total_service_connections']:,}</h2>
            <p style="color: #28a745; margin: 0; font-size: 0.8rem;">+1.8% ▲</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 5px solid #4ecdc4;
            text-align: center;
        ">
            <h4 style="color: #666; margin: 0; font-size: 0.9rem;">WATER QUALITY</h4>
            <h2 style="color: #4ecdc4; margin: 0.5rem 0; font-weight: 700;">{stats['average_water_quality']}%</h2>
            <p style="color: #28a745; margin: 0; font-size: 0.8rem;">+0.2% ▲</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 5px solid #f093fb;
            text-align: center;
        ">
            <h4 style="color: #666; margin: 0; font-size: 0.9rem;">CUSTOMER SATISFACTION</h4>
            <h2 style="color: #f093fb; margin: 0.5rem 0; font-weight: 700;">{stats['customer_satisfaction']}/5</h2>
            <p style="color: #28a745; margin: 0; font-size: 0.8rem;">+0.1 ▲</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-left: 5px solid #ffeaa7;
            text-align: center;
        ">
            <h4 style="color: #666; margin: 0; font-size: 0.9rem;">DAILY PRODUCTION</h4>
            <h2 style="color: #fdcb6e; margin: 0.5rem 0; font-weight: 700;">1.68B</h2>
            <p style="color: #666; margin: 0; font-size: 0.8rem;">Liters/Day</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-time operational dashboard
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🌊 Service Area Performance")
        if areas_data:
            fig = UIComponents.create_consumption_chart(areas_data)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### ⚡ System Health")
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span style="font-weight: 600;">Water Quality</span>
                <span style="color: #28a745; font-weight: 700;">{stats['average_water_quality']}%</span>
            </div>
            <div style="background: #f8f9fa; height: 8px; border-radius: 4px;">
                <div style="background: linear-gradient(90deg, #28a745, #20c997); height: 8px; width: {stats['average_water_quality']}%; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Infrastructure status
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.07);">
            <h4 style="color: #667eea; margin-bottom: 1rem;">🏭 Infrastructure Status</h4>
            <div style="display: grid; gap: 0.8rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span>Treatment Plants</span>
                    <span style="color: #28a745; font-weight: 600;">{stats['treatment_plants']} ✓</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Pumping Stations</span>
                    <span style="color: #28a745; font-weight: 600;">156 ✓</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Pipeline Network</span>
                    <span style="color: #28a745; font-weight: 600;">9,800km ✓</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>System Availability</span>
                    <span style="color: #28a745; font-weight: 600;">99.2% ✓</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Monthly trends section
    st.markdown("### 📈 Monthly Performance Trends")
    if trends_data:
        fig = UIComponents.create_trends_chart(trends_data)
        st.plotly_chart(fig, use_container_width=True)
    
    # AI Foundry modules - integrated view
    st.markdown("## 🤖 AI Foundry Active Modules")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        ">
            <h2 style="margin: 0; color: white;">👥</h2>
            <h3 style="margin: 0.5rem 0; color: white;">HR AI Assistant</h3>
            <p style="margin: 0; opacity: 0.9;">24/7 Employee Support</p>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Active Queries</span>
                    <strong>127</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Resolution Rate</span>
                    <strong>95%</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Avg Response</span>
                    <strong>< 30sec</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4ecdc4, #44a08d);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);
        ">
            <h2 style="margin: 0; color: white;">🎫</h2>
            <h3 style="margin: 0.5rem 0; color: white;">Smart Ticketing</h3>
            <p style="margin: 0; opacity: 0.9;">AI-Powered Classification</p>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Open Tickets</span>
                    <strong>43</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Auto-Classified</span>
                    <strong>97%</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Avg Resolution</span>
                    <strong>4.2hrs</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
        ">
            <h2 style="margin: 0; color: white;">📊</h2>
            <h3 style="margin: 0.5rem 0; color: white;">Data Analytics</h3>
            <p style="margin: 0; opacity: 0.9;">Real-time Insights</p>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Daily Queries</span>
                    <strong>284</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Success Rate</span>
                    <strong>98%</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>Avg Response</span>
                    <strong>< 5sec</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Executive summary and ROI
    st.markdown("## 💼 Executive Summary & ROI Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border-left: 6px solid #667eea;
        ">
            <h3 style="color: #667eea; margin-bottom: 1.5rem;">🎯 Business Impact Metrics</h3>
            <div style="display: grid; gap: 1rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">HR Query Resolution</span>
                    <span style="color: #28a745; font-weight: 700;">99.5% faster</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">Ticket Classification</span>
                    <span style="color: #28a745; font-weight: 700;">95% automated</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">Data Query Speed</span>
                    <span style="color: #28a745; font-weight: 700;">99.9% faster</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0;">
                    <span style="font-weight: 600;">Operational Efficiency</span>
                    <span style="color: #28a745; font-weight: 700;">+40% improvement</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border-left: 6px solid #764ba2;
        ">
            <h3 style="color: #764ba2; margin-bottom: 1.5rem;">💰 ROI & Cost Savings (Annual)</h3>
            <div style="display: grid; gap: 1rem;">
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">HR Automation Savings</span>
                    <span style="color: #28a745; font-weight: 700;">$340,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">Customer Service Efficiency</span>
                    <span style="color: #28a745; font-weight: 700;">$450,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; border-bottom: 1px solid #f0f0f0;">
                    <span style="font-weight: 600;">Data-Driven Optimization</span>
                    <span style="color: #28a745; font-weight: 700;">$670,000</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem 0; background: #f8f9fa; padding-left: 1rem; padding-right: 1rem; border-radius: 8px;">
                    <span style="font-weight: 700; font-size: 1.1rem;">Total Annual ROI</span>
                    <span style="color: #28a745; font-weight: 700; font-size: 1.2rem;">$1.46M</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_hr_assistant():
    """Show HR Assistant page"""
    # Import here to avoid circular imports
    from components.hr_assistant import render_hr_assistant
    render_hr_assistant()

def show_smart_ticketing():
    """Show Smart Ticketing page"""
    from components.smart_ticketing import render_smart_ticketing
    render_smart_ticketing()

def show_chat_with_data():
    """Show Chat with Data page"""
    from components.chat_with_data import render_chat_with_data
    render_chat_with_data()

if __name__ == "__main__":
    main()