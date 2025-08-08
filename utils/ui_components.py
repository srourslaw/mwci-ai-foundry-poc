import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Any
import time

class UIComponents:
    
    @staticmethod
    def render_header(title: str, subtitle: str = "", icon: str = "🌊"):
        """Render page header with Manila Water branding"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #1f77b4, #2ca02c);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        ">
            <h1 style="margin: 0; color: white;">{icon} {title}</h1>
            {f'<p style="margin: 0.5rem 0 0 0; color: #e8f4f8;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title: str, value: str, delta: str = None, icon: str = "📊"):
        """Render metric card with optional delta"""
        delta_html = ""
        if delta:
            delta_color = "green" if delta.startswith("+") else "red" if delta.startswith("-") else "gray"
            delta_html = f'<p style="color: {delta_color}; margin: 0; font-size: 0.9rem;">{delta}</p>'
        
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1f77b4;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">{icon}</span>
                <h4 style="margin: 0; color: #333;">{title}</h4>
            </div>
            <h2 style="margin: 0.5rem 0 0 0; color: #1f77b4;">{value}</h2>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_chat_message(message: str, is_user: bool = False, avatar: str = None):
        """Render chat message with styling"""
        if is_user:
            alignment = "flex-end"
            bg_color = "#1f77b4"
            text_color = "white"
            avatar_icon = "👤" if not avatar else avatar
        else:
            alignment = "flex-start"
            bg_color = "#f0f8ff"
            text_color = "#333"
            avatar_icon = "🤖" if not avatar else avatar
        
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: {alignment};
            margin: 1rem 0;
        ">
            <div style="
                max-width: 70%;
                padding: 1rem;
                border-radius: 15px;
                background-color: {bg_color};
                color: {text_color};
                position: relative;
            ">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span>{avatar_icon}</span>
                    <strong>{'You' if is_user else 'Assistant'}</strong>
                </div>
                <p style="margin: 0;">{message}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_typing_indicator():
        """Show typing indicator animation"""
        with st.empty():
            for i in range(3):
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    margin: 1rem 0;
                ">
                    <div style="
                        padding: 1rem;
                        border-radius: 15px;
                        background-color: #f0f8ff;
                        color: #666;
                    ">
                        <span>🤖 Assistant is typing{'.' * (i + 1)}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.5)
    
    @staticmethod
    def render_employee_card(employee: Dict):
        """Render employee information card"""
        leave_total = sum(employee.get('leave_balance', {}).values())
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f0f8ff, #e6f3ff);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #1f77b4;
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div style="
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: #1f77b4;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                ">
                    👤
                </div>
                <div>
                    <h3 style="margin: 0; color: #1f77b4;">{employee.get('name', 'N/A')}</h3>
                    <p style="margin: 0; color: #666;">{employee.get('position', 'N/A')}</p>
                    <p style="margin: 0; color: #666; font-size: 0.9rem;">{employee.get('department', 'N/A')}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <strong>📧 Email:</strong><br>
                    <span style="color: #666;">{employee.get('email', 'N/A')}</span>
                </div>
                <div>
                    <strong>📍 Location:</strong><br>
                    <span style="color: #666;">{employee.get('location', 'N/A')}</span>
                </div>
                <div>
                    <strong>👔 Manager:</strong><br>
                    <span style="color: #666;">{employee.get('manager', 'N/A')}</span>
                </div>
                <div>
                    <strong>🏖️ Leave Balance:</strong><br>
                    <span style="color: #2ca02c; font-weight: bold;">{leave_total} days</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_ticket_status(ticket: Dict):
        """Render ticket status card"""
        status_colors = {
            "New": "#ff7f0e",
            "In Progress": "#1f77b4", 
            "Resolved": "#2ca02c",
            "Closed": "#666666"
        }
        
        priority_colors = {
            "Critical": "#d62728",
            "High": "#ff7f0e",
            "Medium": "#2ca02c",
            "Low": "#1f77b4"
        }
        
        status_color = status_colors.get(ticket.get('status', 'New'), "#666666")
        priority_color = priority_colors.get(ticket.get('priority', 'Medium'), "#666666")
        
        st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid {status_color};
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 1rem 0;
        ">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #333;">🎫 Ticket {ticket.get('id', 'N/A')}</h4>
                <div style="display: flex; gap: 0.5rem;">
                    <span style="
                        background: {status_color};
                        color: white;
                        padding: 0.3rem 0.8rem;
                        border-radius: 15px;
                        font-size: 0.8rem;
                        font-weight: bold;
                    ">{ticket.get('status', 'New')}</span>
                    <span style="
                        background: {priority_color};
                        color: white;
                        padding: 0.3rem 0.8rem;
                        border-radius: 15px;
                        font-size: 0.8rem;
                        font-weight: bold;
                    ">{ticket.get('priority', 'Medium')}</span>
                </div>
            </div>
            
            <p style="color: #333; margin-bottom: 1rem; line-height: 1.5;">
                <strong>Description:</strong> {ticket.get('description', 'N/A')}
            </p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
                <div>
                    <strong>👤 Customer:</strong><br>
                    {ticket.get('customer_name', 'N/A')}
                </div>
                <div>
                    <strong>📍 Area:</strong><br>
                    {ticket.get('area', 'N/A')}
                </div>
                <div>
                    <strong>🔧 Assigned To:</strong><br>
                    {ticket.get('assigned_tech', 'Unassigned')}
                </div>
                <div>
                    <strong>📅 Created:</strong><br>
                    {ticket.get('created_date', 'N/A')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_consumption_chart(areas_data: List[Dict]) -> go.Figure:
        """Create water consumption chart"""
        df = pd.DataFrame(areas_data)
        
        fig = px.bar(
            df, 
            x='area', 
            y='monthly_consumption_liters',
            title="Monthly Water Consumption by Area",
            labels={'monthly_consumption_liters': 'Consumption (Liters)', 'area': 'Service Area'},
            color='monthly_consumption_liters',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            title_font_size=16,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_quality_gauge(score: float) -> go.Figure:
        """Create water quality gauge chart"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Water Quality Score"},
            delta = {'reference': 95},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 70], 'color': "#ffcccc"},
                    {'range': [70, 90], 'color': "#ffffcc"},
                    {'range': [90, 100], 'color': "#ccffcc"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_trends_chart(trends_data: List[Dict]) -> go.Figure:
        """Create monthly trends chart"""
        df = pd.DataFrame(trends_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Consumption Trend', 'Customer Complaints', 'New Connections', 'Overall Trends'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Consumption trend
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['consumption'], 
                      mode='lines+markers', name='Consumption',
                      line=dict(color='#1f77b4', width=3)),
            row=1, col=1
        )
        
        # Complaints trend
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['complaints'], 
                      mode='lines+markers', name='Complaints',
                      line=dict(color='#d62728', width=3)),
            row=1, col=2
        )
        
        # New connections
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['new_connections'], 
                      mode='lines+markers', name='New Connections',
                      line=dict(color='#2ca02c', width=3)),
            row=2, col=1
        )
        
        # Combined view
        fig.add_trace(
            go.Scatter(x=df['month'], y=df['consumption'], 
                      mode='lines', name='Consumption', 
                      line=dict(color='#1f77b4'), showlegend=False),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text="Manila Water Monthly Performance Trends",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def render_success_message(message: str):
        """Render success message"""
        st.markdown(f"""
        <div style="
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #28a745;
        ">
            <strong>✅ Success:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_error_message(message: str):
        """Render error message"""
        st.markdown(f"""
        <div style="
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #dc3545;
        ">
            <strong>❌ Error:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_info_message(message: str):
        """Render info message"""
        st.markdown(f"""
        <div style="
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #17a2b8;
        ">
            <strong>ℹ️ Info:</strong> {message}
        </div>
        """, unsafe_allow_html=True)