import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.ui_components import UIComponents
from utils.data_processor import get_data_processor
from utils.ai_models import get_ai_manager
import time
import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

def render_smart_ticketing():
    """Render Smart Ticketing page"""
    # Full width header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🎫 Smart Ticketing System</h1>
        <h3 style="margin: 0.5rem 0 0 0; font-weight: 300; opacity: 0.9;">AI-Powered Customer Service & Ticket Management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'tickets' not in st.session_state:
        st.session_state.tickets = []
    
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Load initial sample tickets
    if not st.session_state.tickets:
        st.session_state.tickets = data_processor.get_sample_tickets().copy()
    
    # Top stats dashboard
    st.markdown("## 📊 Ticket Statistics & System Status")
    
    # Stats row
    total_tickets = len(st.session_state.tickets)
    new_tickets = len([t for t in st.session_state.tickets if t.get('status') == 'New'])
    in_progress = len([t for t in st.session_state.tickets if t.get('status') == 'In Progress'])
    resolved = len([t for t in st.session_state.tickets if t.get('status') == 'Resolved'])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📋 Total Tickets", total_tickets)
    with col2:
        st.metric("🆕 New", new_tickets)
    with col3:
        st.metric("⏳ In Progress", in_progress)
    with col4:
        st.metric("✅ Resolved", resolved)
    with col5:
        success_rate = round((resolved / total_tickets * 100), 1) if total_tickets > 0 else 0
        st.metric("📈 Success Rate", f"{success_rate}%")
    
    # Enhanced Technician status section
    st.markdown("### 🔧 Manila Water Technical Team Status")
    technicians = data_processor.get_technicians()
    
    # Create a more sophisticated layout
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(68, 160, 141, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid rgba(78, 205, 196, 0.2);
    ">
        <p style="text-align: center; font-size: 1.1rem; color: #333; margin: 0;">
            Real-time technician availability and workload monitoring
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create enhanced technician cards
    tech_cols = st.columns(len(technicians))
    for i, tech in enumerate(technicians):
        with tech_cols[i]:
            # Determine status styling
            if tech['status'] == 'Available':
                status_color = "#2ecc71"  # Green
                status_icon = "🟢"
                status_bg = "rgba(46, 204, 113, 0.1)"
                status_border = "rgba(46, 204, 113, 0.3)"
            else:
                status_color = "#e74c3c"  # Red
                status_icon = "🔴"
                status_bg = "rgba(231, 76, 60, 0.1)"
                status_border = "rgba(231, 76, 60, 0.3)"
            
            # Calculate workload percentage
            workload_pct = (tech['current_workload'] / tech['max_capacity']) * 100
            
            # Determine workload color
            if workload_pct <= 50:
                workload_color = "#2ecc71"  # Green
            elif workload_pct <= 80:
                workload_color = "#f39c12"  # Orange
            else:
                workload_color = "#e74c3c"  # Red
            
            # Create a clean HTML structure without comments
            tech_html = f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-left: 4px solid {status_color}; margin-bottom: 1rem;">
                <div style="background: {status_bg}; border: 2px solid {status_border}; border-radius: 50%; width: 60px; height: 60px; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                    {status_icon}
                </div>
                <div style="font-weight: 700; font-size: 1.1rem; color: #2c3e50; margin-bottom: 0.5rem;">
                    {tech['name']}
                </div>
                <div style="color: #7f8c8d; font-size: 0.9rem; margin-bottom: 1rem;">
                    {tech['specialty']}
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <div style="color: #34495e; font-size: 0.8rem; margin-bottom: 0.3rem;">
                        Current Workload
                    </div>
                    <div style="background: #ecf0f1; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 0.3rem;">
                        <div style="background: {workload_color}; height: 100%; width: {workload_pct}%; border-radius: 4px;"></div>
                    </div>
                    <div style="color: {workload_color}; font-weight: 600; font-size: 0.9rem;">
                        {tech['current_workload']}/{tech['max_capacity']} tickets ({workload_pct:.0f}%)
                    </div>
                </div>
                <div style="background: rgba(52, 152, 219, 0.1); padding: 0.5rem; border-radius: 6px; color: #2980b9; font-size: 0.85rem; margin-top: 1rem;">
                    📍 Zone: {tech.get('zone', 'Metro Manila')}
                </div>
            </div>
            """
            st.markdown(tech_html, unsafe_allow_html=True)
    
    # Team summary section
    total_technicians = len(technicians)
    available_technicians = len([t for t in technicians if t['status'] == 'Available'])
    total_capacity = sum(tech['max_capacity'] for tech in technicians)
    current_load = sum(tech['current_workload'] for tech in technicians)
    avg_workload = (current_load / total_capacity * 100) if total_capacity > 0 else 0
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
    ">
        <div style="text-align: center;">
            <h4 style="margin: 0 0 1rem 0; color: white;">📊 Team Performance Summary</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                <div style="text-align: center; margin: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold;">{available_technicians}/{total_technicians}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Available Now</div>
                </div>
                <div style="text-align: center; margin: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold;">{avg_workload:.0f}%</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Team Utilization</div>
                </div>
                <div style="text-align: center; margin: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold;">{current_load}/{total_capacity}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Active Tickets</div>
                </div>
                <div style="text-align: center; margin: 0.5rem;">
                    <div style="font-size: 2rem; font-weight: bold;">24/7</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Coverage</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics Section
    st.markdown("## 📊 Ticketing Analytics & Performance")
    render_ticketing_analytics(data_processor, st.session_state.tickets)
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🆕 Create Ticket", "📋 Ticket Dashboard", "🤖 AI Demo"])
    
    with tab1:
        render_create_ticket_tab(data_processor, ai_manager)
    
    with tab2:
        render_ticket_dashboard_tab()
    
    with tab3:
        render_ai_demo_tab(data_processor, ai_manager)

def render_create_ticket_tab(data_processor, ai_manager):
    """Render create ticket tab"""
    st.markdown("### 🎫 Create New Support Ticket")
    
    with st.form("create_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("Customer Name", placeholder="Enter customer name")
            customer_contact = st.text_input("Contact Number", placeholder="+63 XXX XXX XXXX")
            area = st.selectbox("Service Area", [
                "Select area...", "Makati", "Quezon City", "Manila", 
                "Pasig", "Mandaluyong", "Taguig", "BGC"
            ])
        
        with col2:
            priority = st.selectbox("Priority (AI will suggest)", [
                "Let AI Determine", "Critical", "High", "Medium", "Low"
            ])
            category = st.selectbox("Category (AI will suggest)", [
                "Let AI Classify", "Water Quality Issues", "Billing Inquiries", 
                "Service Interruption", "New Connection Request", "Meter Reading Issues"
            ])
        
        description = st.text_area(
            "Issue Description", 
            placeholder="Describe the issue in detail...",
            height=100
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit = st.form_submit_button("🚀 Create Ticket with AI Analysis", use_container_width=True)
    
    if submit and description and customer_name and area != "Select area...":
        create_ticket_with_ai(description, customer_name, customer_contact, area, priority, category, data_processor, ai_manager)
    elif submit:
        UIComponents.render_error_message("Please fill in all required fields")

def create_ticket_with_ai(description, customer_name, contact, area, priority, category, data_processor, ai_manager):
    """Create ticket with AI analysis"""
    with st.spinner("🤖 AI is analyzing the ticket..."):
        # Get ticket categories for classification
        categories = data_processor.get_ticket_categories()
        
        # AI Classification
        classification = ai_manager.classify_ticket(description, categories)
        
        # Use AI suggestions if user selected "Let AI Determine"
        final_category = category if category != "Let AI Classify" else classification.get('category', 'General Inquiry')
        final_priority = priority if priority != "Let AI Determine" else classification.get('priority', 'Medium')
        
        # Find best technician
        best_tech = data_processor.find_best_technician(final_category, area)
        
        # Generate solution suggestion
        solution = ai_manager.suggest_ticket_solution(final_category, description)
        
        # Create ticket
        ticket_id = f"TKT{len(st.session_state.tickets) + 1:03d}"
        new_ticket = {
            'id': ticket_id,
            'description': description,
            'customer_name': customer_name,
            'customer_contact': contact,
            'area': area,
            'status': 'New',
            'priority': final_priority,
            'category': final_category,
            'assigned_tech': best_tech.get('name', 'Unassigned'),
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ai_classification': classification,
            'suggested_solution': solution
        }
        
        st.session_state.tickets.append(new_ticket)
        
        # Show results
        st.success("✅ Ticket created successfully!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🤖 AI Analysis Results")
            st.markdown(f"""
            **Ticket ID:** {ticket_id}  
            **AI Category:** {final_category}  
            **AI Priority:** {final_priority}  
            **Confidence:** {classification.get('confidence', 0):.0%}  
            **Assigned to:** {best_tech.get('name', 'Unassigned')}  
            
            **AI Reasoning:** {classification.get('reasoning', 'Standard classification')}
            """)
        
        with col2:
            st.markdown("#### 💡 AI Solution Suggestion")
            st.markdown(solution)

def render_ticket_dashboard_tab():
    """Render ticket dashboard tab"""
    st.markdown("### 📋 Active Tickets")
    
    if not st.session_state.tickets:
        st.info("No tickets available. Create a new ticket to get started!")
        return
    
    # Filter controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "New", "In Progress", "Resolved"])
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
    
    with col3:
        category_filter = st.selectbox("Filter by Category", [
            "All", "Water Quality Issues", "Billing Inquiries", 
            "Service Interruption", "New Connection Request", "Meter Reading Issues"
        ])
    
    with col4:
        sort_by = st.selectbox("Sort by", ["Created Date", "Priority", "Status"])
    
    # Filter tickets
    filtered_tickets = st.session_state.tickets.copy()
    
    if status_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t.get('status') == status_filter]
    
    if priority_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t.get('priority') == priority_filter]
    
    if category_filter != "All":
        filtered_tickets = [t for t in filtered_tickets if t.get('category') == category_filter]
    
    # Display tickets
    for i, ticket in enumerate(filtered_tickets):
        with st.expander(f"🎫 {ticket['id']} - {ticket['category']} ({ticket['priority']})", expanded=i<3):
            UIComponents.render_ticket_status(ticket)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✅ Resolve", key=f"resolve_{ticket['id']}"):
                    update_ticket_status(ticket['id'], 'Resolved')
            
            with col2:
                if st.button("⏳ In Progress", key=f"progress_{ticket['id']}"):
                    update_ticket_status(ticket['id'], 'In Progress')
            
            with col3:
                if st.button("🔄 Reopen", key=f"reopen_{ticket['id']}"):
                    update_ticket_status(ticket['id'], 'New')
            
            # Show AI insights if available
            if 'ai_classification' in ticket:
                with st.expander("🤖 AI Insights"):
                    st.markdown(f"**Classification Confidence:** {ticket['ai_classification'].get('confidence', 0):.0%}")
                    st.markdown(f"**AI Reasoning:** {ticket['ai_classification'].get('reasoning', 'N/A')}")
                    if 'suggested_solution' in ticket:
                        st.markdown("**Suggested Solution:**")
                        st.markdown(ticket['suggested_solution'])

def render_ai_demo_tab(data_processor, ai_manager):
    """Render AI demo tab"""
    st.markdown("### 🤖 AI Classification Demo")
    st.markdown("Test the AI's ability to classify and route tickets automatically.")
    
    # Sample descriptions for demo
    sample_descriptions = [
        "Water pressure is very low in our building since yesterday",
        "My water bill seems too high this month, please check meter reading", 
        "Water coming out of tap has strange smell and taste",
        "Need to install new water connection for my new house",
        "Water meter is not working properly, showing wrong readings",
        "No water supply in our area since this morning",
        "Want to inquire about payment options for my outstanding bill"
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Enter Issue Description")
        # Initialize session state for demo description
        if "demo_text" not in st.session_state:
            st.session_state.demo_text = ""
            
        demo_description = st.text_area(
            "Description", 
            value=st.session_state.demo_text,
            placeholder="Describe the customer issue...",
            height=100,
            key="demo_description"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎯 Classify with AI", use_container_width=True):
                if demo_description:
                    demo_ai_classification(demo_description, data_processor, ai_manager)
        
        with col_b:
            if st.button("🔄 Clear", use_container_width=True):
                st.session_state.demo_text = ""
                st.rerun()
    
    with col2:
        st.markdown("#### 📝 Quick Test Samples")
        for i, sample in enumerate(sample_descriptions):
            if st.button(f"Test {i+1}", key=f"sample_{i}", help=sample, use_container_width=True):
                st.session_state.demo_text = sample
                st.rerun()

def demo_ai_classification(description, data_processor, ai_manager):
    """Demo AI classification"""
    with st.spinner("🤖 AI is analyzing..."):
        categories = data_processor.get_ticket_categories()
        classification = ai_manager.classify_ticket(description, categories)
        
        # Find best technician
        best_tech = data_processor.find_best_technician(classification.get('category', ''))
        
        # Generate solution
        solution = ai_manager.suggest_ticket_solution(classification.get('category', ''), description)
        
        time.sleep(1)  # Realistic delay
    
    # Display results
    st.markdown("#### 🎯 AI Classification Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **📂 Category:** {classification.get('category', 'Unknown')}  
        **⚡ Priority:** {classification.get('priority', 'Medium')}  
        **🎯 Confidence:** {classification.get('confidence', 0):.0%}  
        **🔧 Assigned To:** {best_tech.get('name', 'Unassigned')}  
        **📍 Zone:** {best_tech.get('zone', 'N/A')}  
        
        **🧠 AI Reasoning:**  
        {classification.get('reasoning', 'Standard classification applied')}
        """)
    
    with col2:
        st.markdown("**💡 Suggested Solution:**")
        st.markdown(solution)
        
        if best_tech:
            st.markdown(f"""
            **👨‍🔧 Technician Info:**  
            **Name:** {best_tech.get('name')}  
            **Specialty:** {best_tech.get('specialty')}  
            **Current Load:** {best_tech.get('current_workload')}/{best_tech.get('max_capacity')}  
            **Status:** {best_tech.get('status')}
            """)

def render_ticketing_analytics(data_processor, tickets):
    """Render comprehensive ticketing analytics and visualizations"""
    
    if not tickets:
        st.warning("No ticket data available for analytics")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ticket Status Distribution
        st.markdown("### 🎫 Ticket Status Distribution")
        status_counts = {}
        for ticket in tickets:
            status = ticket.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Tickets by Status",
            color_discrete_map={
                'New': '#ff7f0e',
                'In Progress': '#4ecdc4', 
                'Resolved': '#2ca02c',
                'Closed': '#666666'
            }
        )
        fig_status.update_layout(height=350)
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Priority Analysis
        st.markdown("### ⚠️ Priority Level Analysis")
        priority_counts = {}
        for ticket in tickets:
            priority = ticket.get('priority', 'Medium')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        fig_priority = px.bar(
            x=list(priority_counts.keys()),
            y=list(priority_counts.values()),
            title="Tickets by Priority Level",
            color=list(priority_counts.keys()),
            color_discrete_map={
                'Critical': '#d62728',
                'High': '#ff7f0e',
                'Medium': '#4ecdc4',
                'Low': '#2ca02c'
            }
        )
        fig_priority.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_priority, use_container_width=True)
    
    # Category and Area Analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Category Distribution
        st.markdown("### 📊 Category Analysis")
        category_counts = {}
        for ticket in tickets:
            category = ticket.get('category', 'Unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        fig_cat = px.bar(
            x=list(category_counts.values()),
            y=list(category_counts.keys()),
            orientation='h',
            title="Tickets by Category",
            color=list(category_counts.values()),
            color_continuous_scale='viridis'
        )
        fig_cat.update_layout(
            height=400, 
            showlegend=False,
            xaxis_title="Number of Tickets",
            yaxis_title="Category"
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Area Distribution
        st.markdown("### 🏘️ Service Area Analysis")
        area_counts = {}
        for ticket in tickets:
            area = ticket.get('area', 'Unknown')
            area_counts[area] = area_counts.get(area, 0) + 1
        
        fig_area = px.bar(
            x=list(area_counts.keys()),
            y=list(area_counts.values()),
            title="Tickets by Service Area",
            color=list(area_counts.values()),
            color_continuous_scale='plasma'
        )
        fig_area.update_layout(
            height=400, 
            xaxis_tickangle=-45, 
            showlegend=False,
            xaxis_title="Service Area",
            yaxis_title="Number of Tickets"
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    with col3:
        # Technician Performance
        st.markdown("### 👨‍🔧 Technician Workload")
        technicians = data_processor.get_technicians()
        
        tech_data = []
        for tech in technicians:
            workload_pct = (tech.get('current_workload', 0) / tech.get('max_capacity', 1)) * 100
            tech_data.append({
                'Technician': tech.get('name', 'Unknown'),
                'Workload_%': workload_pct,
                'Current_Load': tech.get('current_workload', 0),
                'Max_Capacity': tech.get('max_capacity', 1),
                'Specialty': tech.get('specialty', 'General'),
                'Status': tech.get('status', 'Unknown')
            })
        
        df_tech = pd.DataFrame(tech_data)
        fig_tech = px.bar(
            df_tech,
            x='Technician',
            y='Workload_%',
            color='Status',
            title="Technician Workload %",
            hover_data=['Specialty', 'Current_Load', 'Max_Capacity']
        )
        fig_tech.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_tech, use_container_width=True)
    
    # Time-based Analysis (Simulated data for demonstration)
    st.markdown("### 📈 Ticket Trends & Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily ticket creation trend (last 30 days) with today's activity
        st.markdown("#### 📅 Daily Ticket Volume (Last 30 Days)")
        
        # Generate CONSISTENT historical data using session state
        if 'historical_ticket_data' not in st.session_state:
            # Create stable historical data that won't change
            dates = [datetime.now() - timedelta(days=x) for x in range(30, 1, -1)]
            # Use date-based seed for consistent but realistic data
            historical_tickets = []
            for i, date in enumerate(dates):
                # Use date as seed for consistent daily values
                date_seed = int(date.strftime('%Y%m%d')) % 1000
                random.seed(date_seed)
                # Generate realistic patterns (weekends lower, mid-week higher)
                weekday = date.weekday()
                if weekday >= 5:  # Weekend
                    base_tickets = random.randint(8, 15)
                else:  # Weekday
                    base_tickets = random.randint(12, 22)
                historical_tickets.append(base_tickets)
            
            st.session_state.historical_ticket_data = {
                'dates': dates,
                'tickets': historical_tickets
            }
        
        # Get today's ticket count from session state
        today = datetime.now().date()
        today_tickets = len([t for t in st.session_state.tickets if 
                           datetime.strptime(t.get('created_date', ''), '%Y-%m-%d %H:%M:%S').date() == today])
        
        # Combine historical data with today's data
        all_dates = st.session_state.historical_ticket_data['dates'] + [datetime.now()]
        all_tickets = st.session_state.historical_ticket_data['tickets'] + [today_tickets]
        
        # Create single continuous trend dataframe
        trend_df = pd.DataFrame({
            'Date': all_dates,
            'Tickets_Created': all_tickets,
            'Day_Type': ['Historical'] * len(st.session_state.historical_ticket_data['dates']) + ['Today']
        })
        
        # Create single connected line chart
        fig_trend = go.Figure()
        
        # Add the main trend line (historical + today as one connected line)
        fig_trend.add_trace(go.Scatter(
            x=trend_df['Date'],
            y=trend_df['Tickets_Created'],
            mode='lines+markers',
            name='Daily Tickets',
            line=dict(color='#4ecdc4', width=3, shape='spline'),
            marker=dict(
                size=[8] * (len(all_dates)-1) + [15],  # Larger marker for today
                color=['#4ecdc4'] * (len(all_dates)-1) + ['#ff4757'],  # Red for today
                symbol=['circle'] * (len(all_dates)-1) + ['circle'],
                line=dict(width=2, color='white')
            ),
            hovertemplate="<b>%{x|%B %d, %Y}</b><br>" +
                         "Tickets Created: %{y}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="gray",
                font_size=12
            )
        ))
        
        # Add annotation for today's point
        fig_trend.add_annotation(
            x=datetime.now(),
            y=today_tickets,
            text=f"Live: {today_tickets}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#ff4757",
            font=dict(color="#ff4757", size=11, family="Arial"),
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#ff4757",
            borderwidth=1,
            borderpad=4,
            ax=20,
            ay=-30
        )
        
        fig_trend.update_layout(
            title="Daily Ticket Creation Trend",
            xaxis_title="Date",
            yaxis_title="Tickets Created",
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            font=dict(family="Arial", size=11),
            title_font=dict(size=14, color='#333'),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                tickformat='%m/%d'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)'
            )
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Resolution time analysis
        st.markdown("#### ⏱️ Average Resolution Time by Category")
        
        # Sample resolution time data
        resolution_data = {
            'Water Quality Issues': 4.2,
            'Billing Inquiries': 2.1,
            'Service Interruptions': 6.8,
            'New Connections': 12.5,
            'Meter Issues': 3.7
        }
        
        fig_resolution = px.bar(
            x=list(resolution_data.keys()),
            y=list(resolution_data.values()),
            title="Avg Resolution Time (Hours)",
            color=list(resolution_data.values()),
            color_continuous_scale='RdYlGn_r'
        )
        fig_resolution.update_layout(height=350, xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_resolution, use_container_width=True)
    
    # Performance KPIs
    st.markdown("### 🎯 Performance KPIs & Service Level Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calculate first response time (simulated)
        avg_first_response = 1.8  # hours
        st.metric("Avg First Response", f"{avg_first_response}h", delta="-0.3h")
    
    with col2:
        # Customer satisfaction score
        csat_score = 4.2
        st.metric("Customer Satisfaction", f"{csat_score}/5", delta="+0.1")
    
    with col3:
        # SLA compliance
        sla_compliance = 94.5
        st.metric("SLA Compliance", f"{sla_compliance}%", delta="+2.1%")
    
    with col4:
        # Escalation rate
        escalation_rate = 8.2
        st.metric("Escalation Rate", f"{escalation_rate}%", delta="-1.3%")

def update_ticket_status(ticket_id, new_status):
    """Update ticket status"""
    for ticket in st.session_state.tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = new_status
            break
    
    UIComponents.render_success_message(f"Ticket {ticket_id} status updated to {new_status}")
    st.rerun()