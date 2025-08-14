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

def render_hr_assistant():
    """Render HR Assistant page"""
    # Full width header
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
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">👥 HR AI Assistant</h1>
        <h3 style="margin: 0.5rem 0 0 0; font-weight: 300; opacity: 0.9;">24/7 Employee Support & HR Services</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'hr_messages' not in st.session_state:
        st.session_state.hr_messages = []
        st.session_state.hr_messages.append({
            'role': 'assistant',
            'content': """Hello! I'm your Manila Water HR Assistant. I can help you with:

🏖️ **Leave Requests** - Apply for vacation, sick, or emergency leave
📋 **HR Policies** - Information about benefits, policies, and procedures  
🎯 **Onboarding** - Guidance for new employees
💼 **Employee Services** - Payroll, benefits, and general HR inquiries

How can I assist you today?"""
        })
    
    if 'current_employee' not in st.session_state:
        st.session_state.current_employee = None
    
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Top section with employee selection and quick actions
    st.markdown("## 👤 Employee Portal")
    
    # Employee selection and info in main area
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("### Select Employee (Demo)")
        employees = data_processor.get_all_employees()
        employee_names = [emp['name'] for emp in employees]
        
        selected_name = st.selectbox(
            "Choose employee for demo",
            ["Select an employee..."] + employee_names,
            key="employee_selector",
            label_visibility="collapsed"
        )
        
        if selected_name != "Select an employee...":
            st.session_state.current_employee = data_processor.get_employee_by_name(selected_name)
    
    with col2:
        if st.session_state.current_employee:
            st.markdown("### Employee Information")
            UIComponents.render_employee_card(st.session_state.current_employee)
    
    with col3:
        # Employee leave balance (moved here)
        if st.session_state.current_employee:
            st.markdown("### 📊 Your Leave Balance")
            emp = st.session_state.current_employee
            leave_balance = emp.get('leave_balance', {})
            
            st.metric("🏖️ Vacation", f"{leave_balance.get('vacation', 0)} days")
            st.metric("🤒 Sick Days", f"{leave_balance.get('sick', 0)} days")
            st.metric("🆘 Emergency", f"{leave_balance.get('emergency', 0)} days")
    
    # HR Analytics Section
    st.markdown("## 📊 HR Analytics & Insights")
    render_hr_analytics(data_processor)
    
    # Main chat interface - full width
    st.markdown("## 💬 AI Assistant Chat")
    
    # Quick Actions Section - moved near chat interface
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏖️ Request Leave", use_container_width=True):
            add_quick_message("I would like to request vacation leave for next week. Please guide me through the process and let me know what forms or approvals are needed.")
    with col2:
        if st.button("📋 Check Policies", use_container_width=True):
            add_quick_message("Can you explain Manila Water's health insurance benefits, coverage details, and how to make claims?")
    with col3:
        if st.button("💰 Payroll Info", use_container_width=True):
            add_quick_message("When is the next payday and can you explain how my salary breakdown works including deductions and benefits?")
    with col4:
        if st.button("🆘 Get Help", use_container_width=True):
            add_quick_message("I need assistance with Manila Water's employee onboarding process. Can you help me understand the steps and requirements?")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.hr_messages:
            if message['role'] == 'user':
                UIComponents.render_chat_message(message['content'], is_user=True)
            else:
                UIComponents.render_chat_message(message['content'], is_user=False, avatar="🤖")
    
    # Chat input
    user_input = st.chat_input("Type your HR question here...")
    
    if user_input:
        process_hr_query(user_input, data_processor, ai_manager)
    
    # HR Resources Section
    st.markdown("## 📚 HR Resources & Quick Reference")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("📋 Popular Policies"):
            policies = data_processor.get_hr_policies()
            for policy_name, policy_data in policies.items():
                if st.button(policy_data.get('title', policy_name), key=f"policy_{policy_name}", use_container_width=True):
                    add_quick_message(f"Tell me about {policy_data.get('title', policy_name)}")
    
    with col2:
        with st.expander("❓ Common Questions"):
            common_questions = [
                "How do I apply for leave?",
                "What are my health benefits?",
                "When is payday?",
                "How do I update my information?",
                "What training programs are available?"
            ]
            for question in common_questions:
                if st.button(question, key=f"q_{hash(question)}", use_container_width=True):
                    add_quick_message(question)
    
    with col3:
        # Quick reference links
        with st.expander("📚 Quick References"):
            st.markdown("""
            **Popular Resources:**
            - Employee Handbook
            - Benefits Guide  
            - Leave Policies
            - Contact Directory
            - Training Materials
            """)

def render_hr_analytics(data_processor):
    """Render comprehensive HR analytics and visualizations"""
    
    # Get employee data for analytics
    employees = data_processor.get_all_employees()
    
    if not employees:
        st.warning("No employee data available for analytics")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Department Distribution
        st.markdown("### 👥 Department Distribution")
        dept_counts = {}
        for emp in employees:
            dept = emp.get('department', 'Unknown')
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        
        fig_dept = px.pie(
            values=list(dept_counts.values()),
            names=list(dept_counts.keys()),
            title="Employee Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_dept.update_layout(height=350)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Leave Balance Analysis
        st.markdown("### 🏖️ Leave Balance Overview")
        leave_data = []
        for emp in employees:
            leave_balance = emp.get('leave_balance', {})
            leave_data.append({
                'Employee': emp.get('name', 'Unknown'),
                'Vacation': leave_balance.get('vacation', 0),
                'Sick': leave_balance.get('sick', 0),
                'Emergency': leave_balance.get('emergency', 0)
            })
        
        df_leave = pd.DataFrame(leave_data)
        fig_leave = px.bar(
            df_leave.melt(id_vars=['Employee'], var_name='Leave Type', value_name='Days'),
            x='Employee',
            y='Days',
            color='Leave Type',
            title="Leave Balance by Employee",
            color_discrete_map={'Vacation': '#667eea', 'Sick': '#f093fb', 'Emergency': '#4ecdc4'}
        )
        fig_leave.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig_leave, use_container_width=True)
    
    # Employee tenure analysis - Large charts
    st.markdown("### ⏰ Employee Tenure & Position Analysis")
    
    # Prepare tenure data
    tenure_data = []
    current_date = datetime.now()
    
    for emp in employees:
        hire_date = datetime.strptime(emp.get('hire_date', '2020-01-01'), '%Y-%m-%d')
        tenure_years = (current_date - hire_date).days / 365.25
        tenure_data.append({
            'Employee': emp.get('name', 'Unknown'),
            'Department': emp.get('department', 'Unknown'),
            'Tenure_Years': round(tenure_years, 1),
            'Position': emp.get('position', 'Unknown')
        })
    
    df_tenure = pd.DataFrame(tenure_data)
    
    # Large Tenure Analysis Chart
    fig_tenure = px.scatter(
        df_tenure,
        x='Employee',
        y='Tenure_Years',
        color='Department',
        size='Tenure_Years',
        title="📊 Employee Tenure by Department (Years of Service)",
        hover_data=['Position'],
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_tenure.update_layout(
        height=500, 
        xaxis_tickangle=-45,
        font=dict(size=12),
        title_font_size=16
    )
    st.plotly_chart(fig_tenure, use_container_width=True)
    
    # Enhanced Position Distribution - Show only meaningful positions
    position_counts = {}
    for emp in employees:
        position = emp.get('position', 'Unknown')
        position_counts[position] = position_counts.get(position, 0) + 1
    
    # Filter to show only positions with 5+ employees, then group others
    major_positions = {pos: count for pos, count in position_counts.items() if count >= 5}
    
    # Calculate "Other Positions" count
    other_count = sum(count for count in position_counts.values() if count < 5)
    if other_count > 0:
        major_positions['Other Positions'] = other_count
    
    # Create realistic department mapping for major positions
    department_mapping = {
        'Analyst': 'Analytics & Business Intelligence',
        'Administrator': 'Administration',
        'Agent': 'Customer Service',
        'Coordinator': 'Operations Support',
        'Clerk': 'Administration',
        'Engineer': 'Engineering',
        'Generalist': 'Support Services',
        'Designer': 'Engineering & Design',
        'Developer': 'IT & Technology',
        'Operator': 'Operations',
        'Representative': 'Customer Service',
        'Recruiter': 'Human Resources',
        'Specialist': 'Technical Services',
        'Supervisor': 'Management',
        'Support': 'Support Services',
        'Tester': 'Quality Assurance',
        'Accountant': 'Finance',
        'Inspector': 'Quality Assurance',
        'Technician': 'Technical Operations',
        'Other Positions': 'Various Departments'
    }
    
    # Prepare data for grouped visualization
    position_data = []
    for position, count in major_positions.items():
        dept = department_mapping.get(position, 'Other')
        short_pos = position.replace('Representative', 'Rep').replace('Administrator', 'Admin').replace('Coordinator', 'Coord')
        position_data.append({
            'Position': position,
            'Count': count,
            'Department': dept,
            'Short_Position': short_pos
        })
    
    df_positions = pd.DataFrame(position_data)
    df_positions = df_positions.sort_values('Count', ascending=True)  # Sort for horizontal bar
    
    # Create a modern grouped horizontal bar chart
    fig_pos = px.bar(
        df_positions,
        y='Short_Position',
        x='Count', 
        color='Department',
        orientation='h',
        title="👥 Employee Distribution by Position & Department",
        color_discrete_map={
            'Analytics & Business Intelligence': '#667eea',
            'Administration': '#ffeaa7',
            'Customer Service': '#f093fb', 
            'Operations Support': '#4ecdc4',
            'Engineering': '#667eea',
            'Support Services': '#95a5a6',
            'Engineering & Design': '#764ba2',
            'IT & Technology': '#764ba2',
            'Operations': '#4ecdc4',
            'Human Resources': '#74b9ff',
            'Technical Services': '#667eea',
            'Management': '#ff7675',
            'Quality Assurance': '#2ecc71',
            'Finance': '#f39c12',
            'Technical Operations': '#4ecdc4',
            'Various Departments': '#95a5a6',
            'Other': '#95a5a6'
        },
        text='Count'
    )
    
    # Enhanced styling
    fig_pos.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont=dict(size=11, color='#333', family='Arial'),
        marker=dict(
            line=dict(color='white', width=1.5),
            opacity=0.85
        ),
        hovertemplate="<b>%{customdata[0]}</b><br>Department: %{customdata[1]}<br>Employees: %{x}<extra></extra>",
        customdata=df_positions[['Position', 'Department']].values
    )
    
    fig_pos.update_layout(
        height=500,
        font=dict(size=12, family="Arial"),
        title=dict(
            font=dict(size=18, color='#667eea'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Number of Employees",
            title_font=dict(size=14, color='#333'),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            range=[0, max(major_positions.values()) + 2]
        ),
        yaxis=dict(
            title="Position",
            title_font=dict(size=14, color='#333'),
            tickfont=dict(size=10),
            categoryorder='total ascending'
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            title=dict(text="Department", font=dict(size=12, color='#333')),
            font=dict(size=10)
        ),
        plot_bgcolor='rgba(248,249,250,0.4)',
        paper_bgcolor='white',
        margin=dict(l=150, r=140, t=80, b=60)  # More space for legend
    )
    
    st.plotly_chart(fig_pos, use_container_width=True)
    
    # Reorganized HR Metrics, Employee Demo, and Office Locations
    st.markdown("### 📈 HR Metrics & Employee Selection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Key HR Metrics")
        
        total_employees = len(employees)
        avg_vacation_balance = sum(emp.get('leave_balance', {}).get('vacation', 0) for emp in employees) / total_employees
        avg_tenure = sum(tenure['Tenure_Years'] for tenure in tenure_data) / len(tenure_data)
        departments = len(set(emp.get('department', 'Unknown') for emp in employees))
        
        st.metric("Total Employees", total_employees, delta="+2")
        st.metric("Avg Vacation Balance", f"{avg_vacation_balance:.1f} days", delta="+1.2 days")
        st.metric("Avg Tenure", f"{avg_tenure:.1f} years", delta="+0.8 years")
        st.metric("Active Departments", departments)
    
    with col2:
        st.markdown("#### 👤 Select Employee (Demo)")
        employees_list = data_processor.get_all_employees()
        employee_names = [emp['name'] for emp in employees_list]
        
        selected_name = st.selectbox(
            "Choose employee for demo",
            ["Select an employee..."] + employee_names,
            key="employee_selector_analytics",
            label_visibility="collapsed"
        )
        
        if selected_name != "Select an employee...":
            st.session_state.current_employee = data_processor.get_employee_by_name(selected_name)
            
        # Show selected employee info
        if st.session_state.current_employee:
            emp = st.session_state.current_employee
            st.markdown(f"""
            **👤 {emp.get('name')}**  
            **🏢 Department:** {emp.get('department')}  
            **💼 Position:** {emp.get('position')}  
            **📍 Location:** {emp.get('location')}
            """)
    
    # Full-width Office Locations Chart
    st.markdown("### 🗺️ Manila Water Office Locations Distribution")
    
    locations = {}
    for emp in employees:
        location = emp.get('location', 'Unknown')
        locations[location] = locations.get(location, 0) + 1
    
    # Enhanced office locations visualization - full width
    fig_locations = px.bar(
        x=list(locations.keys()),
        y=list(locations.values()),
        title="Manila Water Office Locations - Employee Distribution",
        color=list(locations.values()),
        color_continuous_scale='Plasma',
        text=list(locations.values())
    )
    
    # Enhanced styling for full-width display
    fig_locations.update_traces(
        texttemplate='%{text}',  # Just the number, no "staff" word
        textposition='outside',
        textfont=dict(size=14, color='#333', family='Arial'),
        marker=dict(
            line=dict(color='white', width=2),
            opacity=0.85
        ),
        hovertemplate="<b>%{x}</b><br>Staff Count: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>",
        customdata=[count/sum(locations.values())*100 for count in locations.values()]
    )
    
    fig_locations.update_layout(
        height=500,  # Larger height for full-width
        showlegend=False,
        title=dict(
            font=dict(size=18, color='#667eea', family='Arial'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Office Location",
            title_font=dict(size=15, color='#333'),
            tickangle=-25,
            tickfont=dict(size=10),  # Smaller font size to prevent overlapping
            showgrid=False
        ),
        yaxis=dict(
            title="Number of Employees",
            title_font=dict(size=15, color='#333'),
            tickfont=dict(size=12),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            range=[0, max(locations.values()) + 5]  # Extra space for numbers on top
        ),
        plot_bgcolor='rgba(248,249,250,0.6)',
        paper_bgcolor='white',
        margin=dict(l=70, r=50, t=80, b=120)  # Optimized for full width
    )
    
    st.plotly_chart(fig_locations, use_container_width=True)
    
    # Full-width facility summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_staff = sum(locations.values())
        st.markdown(f"**👥 Total Staff:** {total_staff}")
    with col2:
        st.markdown(f"**🏢 Office Locations:** {len(locations)}")
    with col3:
        st.markdown("**🟢 All Systems Operational**")
    with col4:
        st.markdown("**📡 Real-time Monitoring**")
    
    # Leave usage trends (simulated data for demonstration)
    st.markdown("### 📊 Leave Usage Trends (2024)")
    
    # Generate sample monthly leave data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    leave_trends = pd.DataFrame({
        'Month': months,
        'Vacation': [45, 38, 52, 67, 78, 89, 92, 85, 71, 56, 48, 41],
        'Sick': [23, 28, 31, 26, 22, 18, 15, 19, 25, 29, 34, 38],
        'Emergency': [8, 12, 15, 11, 9, 7, 5, 8, 12, 16, 14, 10]
    })
    
    fig_trends = px.line(
        leave_trends.melt(id_vars=['Month'], var_name='Leave Type', value_name='Days Taken'),
        x='Month',
        y='Days Taken',
        color='Leave Type',
        title="Monthly Leave Usage Trends",
        markers=True,
        color_discrete_map={'Vacation': '#667eea', 'Sick': '#f093fb', 'Emergency': '#4ecdc4'}
    )
    fig_trends.update_layout(height=400)
    st.plotly_chart(fig_trends, use_container_width=True)

def add_quick_message(message):
    """Add a quick message to chat and process it with AI"""
    # Get data processor and AI manager
    data_processor = get_data_processor()
    ai_manager = get_ai_manager()
    
    # Add user message
    st.session_state.hr_messages.append({
        'role': 'user',
        'content': message
    })
    
    # Process with AI immediately
    process_hr_query_immediate(message, data_processor, ai_manager)

def process_hr_query_immediate(user_input, data_processor, ai_manager):
    """Process HR query immediately without showing spinner"""
    # Get employee context
    employee_context = ""
    if st.session_state.current_employee:
        employee_context = f"""
        Current Employee: {st.session_state.current_employee.get('name')}
        Department: {st.session_state.current_employee.get('department')}
        Position: {st.session_state.current_employee.get('position')}
        Leave Balance: {st.session_state.current_employee.get('leave_balance')}
        """
    
    # Prepare additional context based on query type
    additional_context = prepare_hr_context(user_input, data_processor)
    
    # Generate AI response
    response = ai_manager.generate_hr_response(
        user_input, 
        st.session_state.current_employee or {}, 
        f"{employee_context}\n{additional_context}"
    )
    
    # Add assistant response
    st.session_state.hr_messages.append({
        'role': 'assistant',
        'content': response
    })
    
    st.rerun()

def process_hr_query(user_input, data_processor, ai_manager):
    """Process user HR query"""
    # Add user message
    st.session_state.hr_messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Show typing indicator
    with st.spinner("HR Assistant is thinking..."):
        # Get employee context
        employee_context = ""
        if st.session_state.current_employee:
            employee_context = f"""
            Current Employee: {st.session_state.current_employee.get('name')}
            Department: {st.session_state.current_employee.get('department')}
            Position: {st.session_state.current_employee.get('position')}
            Leave Balance: {st.session_state.current_employee.get('leave_balance')}
            """
        
        # Prepare additional context based on query type
        additional_context = prepare_hr_context(user_input, data_processor)
        
        # Generate AI response
        response = ai_manager.generate_hr_response(
            user_input, 
            st.session_state.current_employee or {}, 
            f"{employee_context}\n{additional_context}"
        )
        
        # Add some realistic delay
        time.sleep(random.uniform(1, 2))
    
    # Add assistant response
    st.session_state.hr_messages.append({
        'role': 'assistant',
        'content': response
    })
    
    st.rerun()

def prepare_hr_context(query, data_processor):
    """Prepare additional context based on query type"""
    query_lower = query.lower()
    context = ""
    
    # Leave-related queries
    if any(word in query_lower for word in ['leave', 'vacation', 'sick', 'time off']):
        leave_policies = data_processor.get_leave_policies()
        context += f"\nLeave Policies: {leave_policies}"
    
    # Policy-related queries
    if any(word in query_lower for word in ['policy', 'benefit', 'insurance', 'health']):
        policies = data_processor.get_hr_policies()
        context += f"\nHR Policies: {policies}"
    
    # Onboarding queries
    if any(word in query_lower for word in ['onboard', 'new employee', 'first day', 'start']):
        faq = data_processor.get_onboarding_faq()
        context += f"\nOnboarding FAQ: {faq}"
    
    # Training queries
    if any(word in query_lower for word in ['training', 'development', 'course', 'learning']):
        training_policy = data_processor.get_policy_by_name('training_programs')
        context += f"\nTraining Information: {training_policy}"
    
    return context

# Demo data for realistic interactions
def get_demo_responses():
    """Get demo responses for common queries"""
    return {
        'leave_request': """I can help you with your leave request! Based on your current balance, you have:
        
🏖️ **Vacation Leave**: 15 days available
🤒 **Sick Leave**: 12 days available  
🆘 **Emergency Leave**: 3 days available

To request leave:
1. Specify the type and dates needed
2. I'll check your balance and manager approval requirements
3. Submit the request through our system

What type of leave would you like to request?""",

        'health_benefits': """Manila Water provides comprehensive health benefits:

💊 **Medical Coverage**
- Full medical insurance for you and dependents
- Coverage includes hospitalization, outpatient care, and prescription drugs
- Network of accredited hospitals and clinics

🦷 **Dental & Vision**
- Annual dental checkups and treatments covered
- Vision care including eye exams and prescription glasses

🏥 **Wellness Programs**
- Annual health screening (mandatory and fully covered)
- Mental health support through Employee Assistance Program
- Fitness center memberships and wellness activities

Would you like more details about any specific benefit?""",

        'payroll': """Here's your payroll information:

💰 **Pay Schedule**
- Bi-monthly payroll (15th and 30th of each month)
- Direct deposit to your registered bank account
- Payslips available through employee portal

📊 **Current Deductions**
- SSS, PhilHealth, Pag-IBIG contributions
- Income tax withholding
- Health insurance premiums
- Other voluntary deductions

Need help updating your bank details or understanding deductions?"""
    }