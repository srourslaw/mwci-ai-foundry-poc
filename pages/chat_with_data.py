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
    UIComponents.render_header(
        "Chat with Your Data", 
        "Ask questions about Manila Water's operations in natural language",
        "📊"
    )
    
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
    
    # Sidebar - Data Overview
    with st.sidebar:
        st.markdown("### 📊 Data Overview")
        
        stats = data_processor.get_summary_stats()
        
        UIComponents.render_metric_card(
            "Areas Served", 
            str(len(data_processor.get_service_areas())), 
            icon="🏘️"
        )
        UIComponents.render_metric_card(
            "Total Population", 
            f"{stats['total_population_served']:,}",
            icon="👥"
        )
        UIComponents.render_metric_card(
            "Water Quality", 
            f"{stats['average_water_quality']}%",
            icon="💧"
        )
        
        st.markdown("### 🎯 Quick Queries")
        quick_queries = [
            "Show consumption by area",
            "Water quality summary", 
            "Monthly trends analysis",
            "Infrastructure status",
            "Customer satisfaction metrics",
            "Service area comparison"
        ]
        
        for query in quick_queries:
            if st.button(query, key=f"quick_{hash(query)}", use_container_width=True):
                add_quick_data_message(query)
        
        st.markdown("### 📈 Available Data")
        st.markdown("""
        **Service Areas:** 5 locations  
        **Time Period:** Jan-Jul 2025  
        **Metrics:** Consumption, Quality, Satisfaction  
        **Infrastructure:** Plants, Pipelines, Stations  
        **Real-time:** Quality parameters, Status updates
        """)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
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
    
    with col2:
        # Data insights panel
        render_data_insights_panel(data_processor)

def add_quick_data_message(message):
    """Add a quick message to data chat"""
    st.session_state.data_messages.append({
        'role': 'user',
        'content': message
    })
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