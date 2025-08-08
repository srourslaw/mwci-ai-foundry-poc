import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.ui_components import UIComponents
from utils.data_processor import get_data_processor
from utils.ai_models import get_ai_manager
import time
import random
import datetime

def render_smart_ticketing():
    """Render Smart Ticketing page"""
    UIComponents.render_header(
        "Smart Ticketing System", 
        "AI-powered ticket classification, routing, and resolution",
        "🎫"
    )
    
    # Initialize session state
    if 'tickets' not in st.session_state:
        st.session_state.tickets = []
    
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Load initial sample tickets
    if not st.session_state.tickets:
        st.session_state.tickets = data_processor.get_sample_tickets().copy()
    
    # Sidebar - Ticket Statistics
    with st.sidebar:
        st.markdown("### 📊 Ticket Statistics")
        
        total_tickets = len(st.session_state.tickets)
        new_tickets = len([t for t in st.session_state.tickets if t.get('status') == 'New'])
        in_progress = len([t for t in st.session_state.tickets if t.get('status') == 'In Progress'])
        resolved = len([t for t in st.session_state.tickets if t.get('status') == 'Resolved'])
        
        UIComponents.render_metric_card("Total Tickets", str(total_tickets), icon="📋")
        UIComponents.render_metric_card("New", str(new_tickets), icon="🆕")
        UIComponents.render_metric_card("In Progress", str(in_progress), icon="⏳")
        UIComponents.render_metric_card("Resolved", str(resolved), icon="✅")
        
        st.markdown("### 🔧 Available Technicians")
        technicians = data_processor.get_technicians()
        for tech in technicians:
            status_color = "🟢" if tech['status'] == 'Available' else "🔴"
            workload = f"{tech['current_workload']}/{tech['max_capacity']}"
            st.markdown(f"{status_color} **{tech['name']}**  \n{tech['specialty']} - {workload}")
    
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
            'created_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
        demo_description = st.text_area(
            "Description", 
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
                st.session_state.demo_description = ""
                st.rerun()
    
    with col2:
        st.markdown("#### 📝 Quick Test Samples")
        for i, sample in enumerate(sample_descriptions):
            if st.button(f"Test {i+1}", key=f"sample_{i}", help=sample, use_container_width=True):
                st.session_state.demo_description = sample
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

def update_ticket_status(ticket_id, new_status):
    """Update ticket status"""
    for ticket in st.session_state.tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = new_status
            break
    
    UIComponents.render_success_message(f"Ticket {ticket_id} status updated to {new_status}")
    st.rerun()