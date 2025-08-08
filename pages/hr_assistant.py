import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.ui_components import UIComponents
from utils.data_processor import get_data_processor
from utils.ai_models import get_ai_manager
import time
import random

def render_hr_assistant():
    """Render HR Assistant page"""
    UIComponents.render_header(
        "HR AI Assistant", 
        "Get instant help with HR policies, leave requests, and employee services",
        "👥"
    )
    
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
    
    # Employee selection sidebar
    with st.sidebar:
        st.markdown("### 👤 Employee Login")
        employees = data_processor.get_all_employees()
        employee_names = [emp['name'] for emp in employees]
        
        selected_name = st.selectbox(
            "Select Employee (Demo)",
            ["Select an employee..."] + employee_names,
            key="employee_selector"
        )
        
        if selected_name != "Select an employee...":
            st.session_state.current_employee = data_processor.get_employee_by_name(selected_name)
            
            # Show employee info
            if st.session_state.current_employee:
                UIComponents.render_employee_card(st.session_state.current_employee)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🏖️ Request Leave", use_container_width=True):
            add_quick_message("I need to request vacation leave for next week")
        
        if st.button("📋 Check Policies", use_container_width=True):
            add_quick_message("What are the health insurance benefits?")
        
        if st.button("💰 Payroll Info", use_container_width=True):
            add_quick_message("When is the next payday?")
        
        if st.button("🆘 Help", use_container_width=True):
            add_quick_message("I need help with onboarding process")
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
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
    
    with col2:
        # HR Resources
        st.markdown("### 📚 HR Resources")
        
        with st.expander("📋 Popular Policies"):
            policies = data_processor.get_hr_policies()
            for policy_name, policy_data in policies.items():
                if st.button(policy_data.get('title', policy_name), key=f"policy_{policy_name}", use_container_width=True):
                    add_quick_message(f"Tell me about {policy_data.get('title', policy_name)}")
        
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
        
        # Employee stats (if logged in)
        if st.session_state.current_employee:
            st.markdown("### 📊 Your Status")
            emp = st.session_state.current_employee
            leave_balance = emp.get('leave_balance', {})
            
            UIComponents.render_metric_card(
                "Vacation Days", 
                f"{leave_balance.get('vacation', 0)} days",
                icon="🏖️"
            )
            UIComponents.render_metric_card(
                "Sick Days", 
                f"{leave_balance.get('sick', 0)} days",
                icon="🤒"
            )
            UIComponents.render_metric_card(
                "Emergency Days", 
                f"{leave_balance.get('emergency', 0)} days",
                icon="🆘"
            )

def add_quick_message(message):
    """Add a quick message to chat"""
    st.session_state.hr_messages.append({
        'role': 'user',
        'content': message
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