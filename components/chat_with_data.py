import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.ui_components import UIComponents
from utils.data_processor import get_data_processor
from utils.ai_models import get_ai_manager
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import random

def render_chat_with_data():
    """Render Chat with Data page"""
    # Full width header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">📊 Chat With Data Analytics</h1>
        <h3 style="margin: 0.5rem 0 0 0; font-weight: 300; opacity: 0.9;">Natural Language Queries on Operational Data</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'data_messages' not in st.session_state:
        st.session_state.data_messages = []
        st.session_state.data_messages.append({
            'role': 'assistant',
            'content': """Welcome to Manila Water's Data Analytics Assistant! 🌊📊

I can help you explore our operational data and generate insights. You can ask me questions like:

📈 **Performance Questions:**
- "What's our water consumption trend this year?"
- "Which areas have the highest water quality scores?"
- "How many service connections do we have?"

🔍 **Operational Insights:**
- "Show me areas with service issues"
- "What's our customer satisfaction rate?"
- "Compare consumption between different areas"

📊 **Data Analysis:**
- "Create a chart showing monthly trends"
- "What are our key performance metrics?"
- "Which treatment plants need attention?"

What would you like to know about Manila Water's operations?"""
        })
    
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Top section - Data Overview and Quick Queries
    st.markdown("## 📊 Data Overview & Quick Access")
    
    # Data overview stats
    stats = data_processor.get_summary_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🏘️ Areas Served", len(data_processor.get_service_areas()))
    with col2:
        st.metric("👥 Population", f"{stats['total_population_served']:,}")
    with col3:
        st.metric("💧 Water Quality", f"{stats['average_water_quality']}%")
    with col4:
        st.metric("🏠 Connections", f"{stats['total_service_connections']:,}")
    with col5:
        st.metric("⭐ Satisfaction", f"{stats['customer_satisfaction']}/5")
    
    # Quick query buttons
    st.markdown("### 🎯 Quick Analytics Queries")
    
    quick_queries = [
        "Which service areas have the highest water consumption and quality scores?",
        "Analyze Manila Water's overall performance metrics and identify areas for improvement", 
        "What are the monthly consumption and quality trends across all service areas?",
        "Provide a comprehensive infrastructure status report including treatment plants and pipeline network",
        "How does customer satisfaction vary by service area and what factors might influence it?",
        "Compare the performance between Makati, Manila, and Quezon City service areas"
    ]
    
    # Display quick query buttons
    cols = st.columns(3)
    for i, query in enumerate(quick_queries):
        with cols[i % 3]:
            if st.button(query, key=f"quick_{hash(query)}", use_container_width=True):
                add_quick_data_message(query)
    
    # Available data info
    st.markdown("### 📈 Available Data Sources")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Service Areas:** 5 locations  
        **Time Period:** Jan-Jul 2025  
        **Real-time Updates:** Quality parameters
        """)
    with col2:
        st.markdown("""
        **Metrics:** Consumption, Quality, Satisfaction  
        **Infrastructure:** 8 Plants, 156 Stations  
        **Pipeline Network:** 9,800 km
        """)
    with col3:
        st.markdown("""
        **Data Formats:** Charts, Tables, Reports  
        **AI Analysis:** Trends, Insights, Forecasts  
        **Export Options:** PDF, CSV, Excel
        """)
    
    # Main chat interface - full width
    st.markdown("## 💬 Natural Language Data Queries")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.data_messages:
            if message['role'] == 'user':
                UIComponents.render_chat_message(message['content'], is_user=True)
            else:
                UIComponents.render_chat_message(message['content'], is_user=False, avatar="📊")
                
                # Display charts if available
                if message['role'] == 'assistant' and 'chart_data' in message:
                    render_chart_from_message(message['chart_data'])
    
    # Chat input
    user_input = st.chat_input("Ask about Manila Water's data...")
    
    if user_input:
        process_data_query(user_input, data_processor, ai_manager)

def add_quick_data_message(message):
    """Add a quick message to data chat and process it with AI"""
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Add user message
    st.session_state.data_messages.append({
        'role': 'user',
        'content': message
    })
    
    # Process with AI immediately
    process_data_query_immediate(message, data_processor, ai_manager)

def process_data_query_immediate(user_input, data_processor, ai_manager):
    """Process data query immediately without showing spinner"""
    # Prepare data context based on query
    data_context = prepare_data_context(user_input, data_processor)
    
    # Generate AI response
    response = ai_manager.generate_data_insights(user_input, data_context)
    
    # Check if query needs visualization
    chart_data = None
    if should_create_chart(user_input):
        chart_data = generate_chart_data(user_input, data_processor)
    
    # Add assistant response
    assistant_message = {
        'role': 'assistant',
        'content': response
    }
    
    if chart_data:
        assistant_message['chart_data'] = chart_data
    
    st.session_state.data_messages.append(assistant_message)
    st.rerun()

def process_data_query(user_input, data_processor, ai_manager):
    """Process user data query"""
    # Add user message
    st.session_state.data_messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Show processing indicator
    with st.spinner("📊 Analyzing data..."):
        # Prepare data context based on query
        data_context = prepare_data_context(user_input, data_processor)
        
        # Generate AI response
        response = ai_manager.generate_data_insights(user_input, data_context)
        
        # Check if query needs visualization
        chart_data = None
        if should_create_chart(user_input):
            chart_data = generate_chart_data(user_input, data_processor)
        
        # Add realistic delay
        time.sleep(random.uniform(1, 2))
    
    # Add assistant response
    assistant_message = {
        'role': 'assistant',
        'content': response
    }
    
    if chart_data:
        assistant_message['chart_data'] = chart_data
    
    st.session_state.data_messages.append(assistant_message)
    st.rerun()

def prepare_data_context(query, data_processor):
    """Prepare data context based on query type"""
    query_lower = query.lower()
    context = {}
    
    # Always include summary stats
    context['summary_stats'] = data_processor.get_summary_stats()
    
    # Area/consumption related queries
    if any(word in query_lower for word in ['area', 'consumption', 'usage', 'demand']):
        context['service_areas'] = data_processor.get_service_areas()
    
    # Quality related queries
    if any(word in query_lower for word in ['quality', 'standard', 'parameters', 'compliance']):
        context['water_quality'] = data_processor.get_water_quality_params()
        context['service_areas'] = data_processor.get_service_areas()
    
    # Trends/time series queries
    if any(word in query_lower for word in ['trend', 'monthly', 'time', 'over time', 'growth']):
        context['monthly_trends'] = data_processor.get_monthly_trends()
    
    # Infrastructure queries
    if any(word in query_lower for word in ['infrastructure', 'plant', 'pipeline', 'facility']):
        context['infrastructure'] = data_processor.get_infrastructure_status()
    
    # Operational metrics
    if any(word in query_lower for word in ['metric', 'performance', 'operational', 'efficiency']):
        context['operational_metrics'] = data_processor.get_operational_metrics()
    
    return context

def should_create_chart(query):
    """Determine if query should generate a chart"""
    chart_keywords = [
        'show', 'chart', 'graph', 'plot', 'visualize', 'compare', 
        'trend', 'breakdown', 'distribution', 'analysis'
    ]
    return any(keyword in query.lower() for keyword in chart_keywords)

def generate_chart_data(query, data_processor):
    """Generate appropriate chart based on query"""
    query_lower = query.lower()
    
    # Consumption charts
    if any(word in query_lower for word in ['consumption', 'usage', 'demand', 'area']):
        areas_data = data_processor.get_service_areas()
        return {
            'type': 'consumption_bar',
            'data': areas_data,
            'title': 'Water Consumption by Service Area'
        }
    
    # Quality charts
    elif any(word in query_lower for word in ['quality', 'compliance', 'standard']):
        areas_data = data_processor.get_service_areas()
        return {
            'type': 'quality_bar',
            'data': areas_data,
            'title': 'Water Quality Scores by Area'
        }
    
    # Trends charts
    elif any(word in query_lower for word in ['trend', 'monthly', 'time', 'over time']):
        trends_data = data_processor.get_monthly_trends()
        return {
            'type': 'trends_line',
            'data': trends_data,
            'title': 'Monthly Performance Trends'
        }
    
    # Population vs consumption
    elif any(word in query_lower for word in ['population', 'demographic', 'correlation']):
        areas_data = data_processor.get_service_areas()
        return {
            'type': 'scatter',
            'data': areas_data,
            'title': 'Population vs Water Consumption'
        }
    
    return None

def render_chart_from_message(chart_data):
    """Render chart based on chart_data"""
    if not chart_data:
        return
    
    chart_type = chart_data['type']
    data = chart_data['data']
    title = chart_data['title']
    
    if chart_type == 'consumption_bar':
        df = pd.DataFrame(data)
        fig = px.bar(
            df, 
            x='area', 
            y='monthly_consumption_liters',
            title=title,
            color='monthly_consumption_liters',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title="Service Area",
            yaxis_title="Monthly Consumption (Liters)",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == 'quality_bar':
        df = pd.DataFrame(data)
        fig = px.bar(
            df, 
            x='area', 
            y='water_quality_score',
            title=title,
            color='water_quality_score',
            color_continuous_scale='Greens'
        )
        fig.update_layout(
            xaxis_title="Service Area",
            yaxis_title="Water Quality Score (%)",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == 'trends_line':
        df = pd.DataFrame(data)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['month'], 
            y=df['consumption'],
            mode='lines+markers',
            name='Consumption',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['month'], 
            y=df['complaints'],
            mode='lines+markers',
            name='Complaints',
            yaxis='y2',
            line=dict(color='#d62728', width=3)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Month",
            yaxis=dict(title="Consumption", side="left"),
            yaxis2=dict(title="Complaints", side="right", overlaying="y"),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == 'scatter':
        df = pd.DataFrame(data)
        fig = px.scatter(
            df, 
            x='population', 
            y='monthly_consumption_liters',
            size='service_connections',
            color='water_quality_score',
            hover_name='area',
            title=title
        )
        fig.update_layout(
            xaxis_title="Population",
            yaxis_title="Monthly Consumption (Liters)",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_data_insights_panel(data_processor):
    """Render data insights panel"""
    st.markdown("### 💡 Key Insights")
    
    # Get current data
    stats = data_processor.get_summary_stats()
    areas = data_processor.get_service_areas()
    trends = data_processor.get_monthly_trends()
    
    # Top performing areas
    with st.expander("🏆 Top Performing Areas"):
        top_areas = sorted(areas, key=lambda x: x.get('water_quality_score', 0), reverse=True)[:3]
        for i, area in enumerate(top_areas):
            st.markdown(f"""
            **{i+1}. {area['area']}**  
            Quality: {area['water_quality_score']}%  
            Availability: {area['service_availability']}%
            """)
    
    # Recent trends
    with st.expander("📈 Recent Trends"):
        if len(trends) >= 2:
            latest = trends[-1]
            previous = trends[-2]
            
            consumption_change = ((latest['consumption'] - previous['consumption']) / previous['consumption']) * 100
            complaints_change = ((latest['complaints'] - previous['complaints']) / previous['complaints']) * 100
            
            st.markdown(f"""
            **Latest Month: {latest['month']}**  
            
            Consumption: {consumption_change:+.1f}%  
            Complaints: {complaints_change:+.1f}%  
            New Connections: {latest['new_connections']}
            """)
    
    # Data freshness
    with st.expander("🕒 Data Freshness"):
        st.markdown("""
        **Last Updated:**  
        Water Quality: Today 08:00 AM  
        Consumption Data: Real-time  
        Customer Metrics: Yesterday  
        Infrastructure: Live monitoring
        """)
    
    # Suggested queries
    st.markdown("### 🎯 Try These Queries")
    
    suggested_queries = [
        "Which area consumes the most water?",
        "Show me the quality trends",
        "What's our best performing metric?",
        "Compare Makati and Manila consumption",
        "Infrastructure status summary",
        "Customer satisfaction by area"
    ]
    
    for query in suggested_queries:
        if st.button(f"💬 {query}", key=f"suggest_{hash(query)}", use_container_width=True):
            # Add to chat
            st.session_state.data_messages.append({
                'role': 'user',
                'content': query
            })
            st.rerun()