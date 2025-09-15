import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import time
from utils.ui_components import UIComponents
try:
    from utils.ai_models import get_ai_manager
except ImportError:
    def get_ai_manager():
        return None
from utils.data_processor import get_data_processor

def show_ceo_demo_dashboard():
    """
    CEO Show & Tell Dashboard - Multi-Perspective AI Capabilities Demo
    Designed specifically for executive presentations showing business value
    """

    # Initialize components
    data_processor = get_data_processor()

    # Check for AI configuration
    ai_manager = get_ai_manager()
    show_ai_fallback = not (st.session_state.get('gemini_api_key') or st.session_state.get('openai_api_key'))

    # Header - Executive Presentation Style
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    ">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🚀 AI Business Transformation</h1>
        <h2 style="margin: 1rem 0 0 0; font-weight: 300; opacity: 0.9;">CEO Executive Demonstration</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.2rem; opacity: 0.8;">Four Core AI Capabilities Delivering Measurable ROI</p>
    </div>
    """, unsafe_allow_html=True)

    # ROI Summary Cards at Top
    render_roi_summary()

    # Main Demo Sections
    st.markdown("---")
    st.markdown("## 🎯 Live AI Capability Demonstrations")

    # Demo Navigation
    demo_tab = st.selectbox(
        "🎭 Select Demo Scenario",
        [
            "🏠 Overview: All Capabilities at a Glance",
            "💼 Capability 1: Instant Employee Self-Service",
            "🔍 Capability 2: Proactive Business Intelligence",
            "⚡ Capability 3: Smart Decision Support",
            "🤖 Capability 4: Intelligent Automation",
            "📊 Complete ROI Analysis"
        ],
        help="Choose which AI capability to demonstrate"
    )

    if demo_tab == "🏠 Overview: All Capabilities at a Glance":
        render_capabilities_overview(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "💼 Capability 1: Instant Employee Self-Service":
        render_employee_self_service_demo(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "🔍 Capability 2: Proactive Business Intelligence":
        render_business_intelligence_demo(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "⚡ Capability 3: Smart Decision Support":
        render_decision_support_demo(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "🤖 Capability 4: Intelligent Automation":
        render_intelligent_automation_demo(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "📊 Complete ROI Analysis":
        render_complete_roi_analysis(data_processor)

def render_roi_summary():
    """Executive ROI Summary Cards"""
    st.markdown("### 💰 Business Impact Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 20px rgba(255,107,107,0.3);
        ">
            <h2 style="margin: 0; font-size: 2.5rem;">₱73M</h2>
            <h4 style="margin: 0.5rem 0 0 0;">Annual ROI</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">8-month payback</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4ecdc4, #44a08d);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 20px rgba(78,205,196,0.3);
        ">
            <h2 style="margin: 0; font-size: 2.5rem;">80%</h2>
            <h4 style="margin: 0.5rem 0 0 0;">HR Efficiency</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Query reduction</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #feca57, #ff9ff3);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 20px rgba(254,202,87,0.3);
        ">
            <h2 style="margin: 0; font-size: 2.5rem;">95%</h2>
            <h4 style="margin: 0.5rem 0 0 0;">Response Accuracy</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Emergency classification</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8e6cf, #88d8a3);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 20px rgba(168,230,207,0.3);
        ">
            <h2 style="margin: 0; font-size: 2.5rem;">24/7</h2>
            <h4 style="margin: 0.5rem 0 0 0;">AI Availability</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">No downtime</p>
        </div>
        """, unsafe_allow_html=True)

def render_capabilities_overview(data_processor, ai_manager, show_ai_fallback):
    """Overview of all four AI capabilities"""
    st.markdown("### 🎯 Four AI Capabilities Transforming Business Operations")

    # Visual capability matrix
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
        ">
            <h3>💼 Capability 1: Instant Self-Service</h3>
            <p><strong>User Perspective:</strong> 24/7 access to personal information</p>
            <p><strong>Business Perspective:</strong> 80% reduction in HR workload</p>
            <p><strong>ROI:</strong> ₱17M annually</p>
            <ul>
                <li>Leave balance queries: 2 seconds vs 2 days</li>
                <li>Policy information: Instant vs manual lookup</li>
                <li>Process guidance: Step-by-step automation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
        ">
            <h3>⚡ Capability 3: Smart Decision Support</h3>
            <p><strong>Agent Perspective:</strong> AI-powered classification and routing</p>
            <p><strong>Management Perspective:</strong> Eliminated human error in emergencies</p>
            <p><strong>ROI:</strong> ₱20M in prevented losses</p>
            <ul>
                <li>Emergency response: 95% accuracy</li>
                <li>Technician matching: Optimal resource allocation</li>
                <li>Solution suggestions: Expert-level guidance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4ecdc4, #44a08d);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
        ">
            <h3>🔍 Capability 2: Proactive Intelligence</h3>
            <p><strong>Executive Perspective:</strong> Real-time business insights</p>
            <p><strong>Operations Perspective:</strong> Predictive problem detection</p>
            <p><strong>ROI:</strong> ₱25M in risk prevention</p>
            <ul>
                <li>Compliance monitoring: Continuous oversight</li>
                <li>Trend analysis: Early warning systems</li>
                <li>Performance gaps: Proactive identification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #feca57, #ff9ff3);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            margin-bottom: 1rem;
        ">
            <h3>🤖 Capability 4: Intelligent Automation</h3>
            <p><strong>System Perspective:</strong> End-to-end workflow execution</p>
            <p><strong>Audit Perspective:</strong> Complete traceability</p>
            <p><strong>ROI:</strong> ₱11M efficiency gains</p>
            <ul>
                <li>Automated scheduling: No manual coordination</li>
                <li>Work order creation: Instant execution</li>
                <li>Alert systems: Proactive notifications</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Live metrics
    st.markdown("### 📈 Real-Time Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("HR Queries Handled", "1,247", "↑ 340 today")
    with col2:
        st.metric("Compliance Checks", "89", "↑ 12 today")
    with col3:
        st.metric("Tickets Classified", "156", "↑ 23 today")
    with col4:
        st.metric("Automated Actions", "67", "↑ 8 today")

def render_employee_self_service_demo(data_processor, ai_manager, show_ai_fallback):
    """Employee self-service capability demo"""
    st.markdown("### 💼 Capability 1: Instant Employee Self-Service")

    # Perspective selector
    perspective = st.radio(
        "👀 View from perspective:",
        ["👤 Employee Experience", "🏢 HR Department Impact"],
        horizontal=True
    )

    if perspective == "👤 Employee Experience":
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin-bottom: 2rem;
        ">
            <h4>🎭 Scenario: Maria Santos needs leave information</h4>
            <p><strong>Before AI:</strong> Call HR → Wait for callback → Get information (2-3 days)</p>
            <p><strong>With AI:</strong> Login → Ask question → Get instant answer (2 seconds)</p>
        </div>
        """, unsafe_allow_html=True)

        # Employee simulation
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### 👤 Employee Login Simulation")
            selected_employee = st.selectbox(
                "Select Employee (simulating secure login)",
                ["Maria Santos", "Juan Dela Cruz", "Carmen Lopez", "Roberto Silva"],
                help="In production, employee sees only their own data"
            )

            employee_data = get_employee_demo_data(selected_employee)

            st.markdown(f"""
            **Logged in as:** {selected_employee}
            **Department:** {employee_data['department']}
            **Security Level:** Personal data only
            """)

        with col2:
            st.markdown("#### 💬 AI Assistant Chat")

            # Demo questions
            demo_questions = [
                "How many days leave do I have left?",
                "How do I request emergency leave?",
                "What's my manager's contact information?",
                "How do I log into the HR system?",
                "What training courses are available for me?"
            ]

            selected_question = st.selectbox("Try a question:", demo_questions)

            if st.button("🚀 Ask AI Assistant", use_container_width=True):
                render_employee_ai_response(selected_question, employee_data, show_ai_fallback)

    else:  # HR Department Impact
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #28a745;
            margin-bottom: 2rem;
        ">
            <h4>🏢 HR Department Transformation</h4>
            <p><strong>Before AI:</strong> 120 queries/day → 8 hours handling routine questions</p>
            <p><strong>With AI:</strong> 24 complex queries/day → 6 hours on strategic initiatives</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # HR workload comparison
            fig = go.Figure(data=[
                go.Bar(name='Before AI', x=['Routine Queries', 'Strategic Work'], y=[80, 20], marker_color='#ff6b6b'),
                go.Bar(name='With AI', x=['Routine Queries', 'Strategic Work'], y=[20, 80], marker_color='#4ecdc4')
            ])
            fig.update_layout(
                title="HR Time Allocation (%)",
                yaxis_title="Percentage of Time",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Cost savings breakdown
            st.markdown("#### 💰 Annual Cost Savings")
            savings_data = {
                'Category': ['Staff Time Saved', 'Error Reduction', 'Faster Resolution', 'Employee Satisfaction'],
                'Savings (₱M)': [12, 2.5, 1.8, 0.7]
            }

            fig2 = px.pie(
                values=savings_data['Savings (₱M)'],
                names=savings_data['Category'],
                title="HR Cost Savings Breakdown"
            )
            st.plotly_chart(fig2, use_container_width=True)

def render_business_intelligence_demo(data_processor, ai_manager, show_ai_fallback):
    """Business intelligence capability demo"""
    st.markdown("### 🔍 Capability 2: Proactive Business Intelligence")

    perspective = st.radio(
        "👀 View from perspective:",
        ["📊 Executive Dashboard", "⚠️ Risk Management", "📈 Operational Intelligence"],
        horizontal=True
    )

    if perspective == "📊 Executive Dashboard":
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin-bottom: 2rem;
        ">
            <h4>🎭 Scenario: CEO needs compliance status for board meeting</h4>
            <p><strong>Before AI:</strong> Request report → Wait 2-3 days → Get static document</p>
            <p><strong>With AI:</strong> Ask question → Get real-time analysis → Drill down instantly</p>
        </div>
        """, unsafe_allow_html=True)

        # Live query demo
        query_options = [
            "Are we compliant with DOH water quality standards?",
            "Which service areas need immediate attention?",
            "What's our customer satisfaction trend?",
            "Show me revenue impact of service interruptions",
            "Which areas have declining performance?"
        ]

        selected_query = st.selectbox("Executive Query:", query_options)

        if st.button("🔍 Get AI Analysis", use_container_width=True):
            render_business_intelligence_response(selected_query, data_processor, show_ai_fallback)

    elif perspective == "⚠️ Risk Management":
        render_risk_management_view(data_processor)

    else:  # Operational Intelligence
        render_operational_intelligence_view(data_processor)

def render_decision_support_demo(data_processor, ai_manager, show_ai_fallback):
    """Decision support capability demo"""
    st.markdown("### ⚡ Capability 3: Smart Decision Support")

    perspective = st.radio(
        "👀 View from perspective:",
        ["🎧 Customer Service Agent", "👨‍💼 Operations Manager", "🚨 Emergency Response"],
        horizontal=True
    )

    if perspective == "🎧 Customer Service Agent":
        st.markdown("""
        <div style="
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border-left: 5px solid #ff6b6b;
            margin-bottom: 2rem;
        ">
            <h4>🎭 Scenario: Customer calls with emergency</h4>
            <p><strong>Agent's Challenge:</strong> Classify urgency → Assign technician → Provide timeline</p>
            <p><strong>AI Solution:</strong> Instant classification with confidence scores and recommendations</p>
        </div>
        """, unsafe_allow_html=True)

        # Ticket creation simulator
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📞 Customer Call Simulation")

            emergency_scenarios = [
                "Major water main break on Ayala Avenue causing street flooding",
                "Water has brown color and metallic taste in BGC office building",
                "No water supply in our Makati condominium since morning",
                "Low water pressure affecting entire Pasig subdivision",
                "Water meter showing unusually high readings"
            ]

            customer_issue = st.selectbox("Customer describes issue:", emergency_scenarios)
            customer_name = st.text_input("Customer Name:", "Roberto Silva")
            customer_area = st.selectbox("Service Area:", ["Makati", "BGC", "Pasig", "Quezon City", "Manila"])

            if st.button("🤖 Classify with AI", use_container_width=True):
                render_ticket_classification_demo(customer_issue, customer_name, customer_area, data_processor, show_ai_fallback)

        with col2:
            st.markdown("#### 📊 Agent Performance Impact")

            # Before/After metrics
            metrics_data = pd.DataFrame({
                'Metric': ['Avg Call Time', 'Classification Accuracy', 'Customer Satisfaction', 'Resolution Time'],
                'Before AI': [8.5, 75, 3.2, 24],
                'With AI': [3.2, 95, 4.6, 8]
            })

            fig = go.Figure(data=[
                go.Bar(name='Before AI', x=metrics_data['Metric'], y=metrics_data['Before AI'], marker_color='#ff6b6b'),
                go.Bar(name='With AI', x=metrics_data['Metric'], y=metrics_data['With AI'], marker_color='#4ecdc4')
            ])
            fig.update_layout(title="Agent Performance Improvement", barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)

    elif perspective == "👨‍💼 Operations Manager":
        render_operations_manager_view(data_processor)

    else:  # Emergency Response
        render_emergency_response_view(data_processor)

def render_intelligent_automation_demo(data_processor, ai_manager, show_ai_fallback):
    """Intelligent automation capability demo"""
    st.markdown("### 🤖 Capability 4: Intelligent Automation")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #feca57, #ff9ff3);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    ">
        <h4>🎯 Agentic AI: From Analysis to Action</h4>
        <p>AI doesn't just identify problems - it offers to solve them automatically</p>
    </div>
    """, unsafe_allow_html=True)

    # Automation workflow demo
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🔍 AI Problem Detection")

        # Simulated problem detection
        if st.button("🚨 Simulate AI Detection", use_container_width=True):
            with st.spinner("AI scanning systems..."):
                time.sleep(2)

                st.markdown("""
                <div style="
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                ">
                    <h5>⚠️ AI Alert: Compliance Issue Detected</h5>
                    <p><strong>Issue:</strong> Water quality in Malabon area trending below 98.5% threshold</p>
                    <p><strong>Risk:</strong> Potential regulatory non-compliance in 72 hours</p>
                    <p><strong>Impact:</strong> ₱2.1M penalty risk + service disruption</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### 🤖 AI Suggested Actions")
                st.markdown("""
                **AI:** "I've detected a compliance risk. Would you like me to:"

                ✅ **Schedule emergency water quality testing for tomorrow?**
                ✅ **Create maintenance work orders for pipe inspection?**
                ✅ **Alert the Operations Director via Teams?**
                ✅ **Generate regulatory compliance report?**
                ✅ **Notify affected customers about potential service maintenance?**
                """)

    with col2:
        st.markdown("#### ⚡ Automation Execution")

        if st.button("✅ Execute All Actions", use_container_width=True):
            with st.spinner("AI executing automation workflow..."):
                time.sleep(1)

                progress_bar = st.progress(0)

                actions = [
                    "🧪 Scheduled water quality testing - Lab Team notified",
                    "🔧 Created 3 maintenance work orders - WO-2025-089, WO-2025-090, WO-2025-091",
                    "📢 Alert sent to Operations Director - Teams notification delivered",
                    "📋 Compliance report generated - DOH-COMPLIANCE-2025-08-08.pdf",
                    "📱 Customer notifications prepared - 2,847 affected customers"
                ]

                for i, action in enumerate(actions):
                    time.sleep(0.8)
                    progress_bar.progress((i + 1) / len(actions))
                    st.success(action)

                st.markdown("""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                ">
                    <h5>✅ Automation Complete</h5>
                    <p><strong>Total Time:</strong> 4.2 seconds</p>
                    <p><strong>Manual Time Saved:</strong> 6-8 hours</p>
                    <p><strong>Actions Logged:</strong> Full audit trail created</p>
                    <p><strong>Next Review:</strong> 24 hours (automated)</p>
                </div>
                """, unsafe_allow_html=True)

        # Automation metrics
        st.markdown("#### 📊 Automation Impact")

        automation_metrics = {
            'Process': ['Problem Detection', 'Solution Planning', 'Task Creation', 'Stakeholder Notification', 'Documentation'],
            'Manual Time (hrs)': [2, 1.5, 2, 0.5, 2],
            'AI Time (min)': [0.1, 0.1, 0.1, 0.1, 0.1]
        }

        df = pd.DataFrame(automation_metrics)
        fig = go.Figure(data=[
            go.Bar(name='Manual Process', x=df['Process'], y=df['Manual Time (hrs)'], marker_color='#ff6b6b'),
            go.Bar(name='AI Automation', x=df['Process'], y=[x/60 for x in df['AI Time (min)']], marker_color='#4ecdc4')
        ])
        fig.update_layout(title="Time Savings by Process", yaxis_title="Hours", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

def render_complete_roi_analysis(data_processor):
    """Complete ROI analysis"""
    st.markdown("### 📊 Complete ROI Analysis")

    # Financial impact breakdown
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💰 Annual Cost Savings by Capability")

        roi_data = {
            'Capability': ['Employee Self-Service', 'Business Intelligence', 'Decision Support', 'Intelligent Automation'],
            'Annual Savings (₱M)': [17, 25, 20, 11],
            'Implementation Cost (₱M)': [3, 4, 3, 2]
        }

        fig = go.Figure(data=[
            go.Bar(name='Annual Savings', x=roi_data['Capability'], y=roi_data['Annual Savings (₱M)'], marker_color='#4ecdc4'),
            go.Bar(name='Implementation Cost', x=roi_data['Capability'], y=roi_data['Implementation Cost (₱M)'], marker_color='#ff6b6b')
        ])
        fig.update_layout(title="Cost-Benefit Analysis", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📈 ROI Timeline")

        months = list(range(1, 25))
        cumulative_savings = [i * 6.08 - 12 for i in months]  # ₱73M / 12 months - ₱12M initial cost

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=months, y=cumulative_savings, mode='lines+markers', name='Cumulative ROI', line=dict(color='#4ecdc4', width=3)))
        fig2.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig2.update_layout(title="24-Month ROI Projection", xaxis_title="Months", yaxis_title="ROI (₱M)", height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Detailed metrics
    st.markdown("#### 📊 Detailed Performance Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🏢 Operational Efficiency**
        - HR Query Resolution: 99.5% faster
        - Emergency Response: 18 min avg (was 45 min)
        - Compliance Monitoring: Real-time vs weekly
        - Process Automation: 87% of routine tasks
        """)

    with col2:
        st.markdown("""
        **👥 Employee Impact**
        - Self-Service Adoption: 94%
        - Employee Satisfaction: +1.2 points
        - Training Time Reduction: 60%
        - HR Ticket Volume: -80%
        """)

    with col3:
        st.markdown("""
        **🎯 Business Outcomes**
        - Customer Satisfaction: +0.4 points
        - Regulatory Compliance: 100%
        - Error Reduction: 95%
        - Decision Speed: 10x faster
        """)

# Helper functions for demo responses

def get_employee_demo_data(employee_name):
    """Get demo employee data"""
    employees = {
        "Maria Santos": {
            "department": "Engineering",
            "position": "Senior Engineer",
            "leave_balance": {"vacation": 12, "sick": 8, "emergency": 5},
            "manager": "Juan Rodriguez"
        },
        "Juan Dela Cruz": {
            "department": "Operations",
            "position": "Field Supervisor",
            "leave_balance": {"vacation": 15, "sick": 10, "emergency": 3},
            "manager": "Carmen Lopez"
        },
        "Carmen Lopez": {
            "department": "Customer Service",
            "position": "Service Manager",
            "leave_balance": {"vacation": 8, "sick": 12, "emergency": 7},
            "manager": "Roberto Silva"
        },
        "Roberto Silva": {
            "department": "Finance",
            "position": "Financial Analyst",
            "leave_balance": {"vacation": 10, "sick": 6, "emergency": 4},
            "manager": "Maria Santos"
        }
    }
    return employees.get(employee_name, employees["Maria Santos"])

def render_employee_ai_response(question, employee_data, show_ai_fallback):
    """Render AI response for employee questions"""
    with st.spinner("AI processing your request..."):
        time.sleep(1)

        if "leave" in question.lower():
            total_leave = sum(employee_data['leave_balance'].values())
            st.markdown(f"""
            <div style="
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Assistant Response</h5>
                <p><strong>Your Leave Balance:</strong></p>
                <ul>
                    <li>Vacation Leave: {employee_data['leave_balance']['vacation']} days</li>
                    <li>Sick Leave: {employee_data['leave_balance']['sick']} days</li>
                    <li>Emergency Leave: {employee_data['leave_balance']['emergency']} days</li>
                </ul>
                <p><strong>Total Available:</strong> {total_leave} days</p>
                <p><em>Response time: 1.8 seconds</em></p>
            </div>
            """, unsafe_allow_html=True)

        elif "emergency leave" in question.lower():
            st.markdown(f"""
            <div style="
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Assistant Response</h5>
                <p><strong>Emergency Leave Process:</strong></p>
                <ol>
                    <li>Submit Form HR-204 in employee portal</li>
                    <li>Provide brief explanation of emergency</li>
                    <li>Auto-approval for up to 3 days (you have {employee_data['leave_balance']['emergency']} available)</li>
                    <li>Manager {employee_data['manager']} will be notified automatically</li>
                </ol>
                <p><strong>Need help submitting?</strong> I can guide you through the form.</p>
                <p><em>Response time: 2.1 seconds</em></p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div style="
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Assistant Response</h5>
                <p>I can help you with that! Here's the information you need for your department ({employee_data['department']}).</p>
                <p>For specific system access, contact your manager {employee_data['manager']} or IT helpdesk at ext. 7888.</p>
                <p><em>Response time: 1.2 seconds</em></p>
            </div>
            """, unsafe_allow_html=True)

def render_business_intelligence_response(query, data_processor, show_ai_fallback):
    """Render business intelligence response"""
    with st.spinner("AI analyzing business data..."):
        time.sleep(2)

        if "compliant" in query.lower():
            st.markdown("""
            <div style="
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Compliance Analysis</h5>
                <p><strong>Overall DOH Compliance Status: ✅ COMPLIANT</strong></p>

                <p><strong>Quality Performance Across 16 Service Areas:</strong></p>
                <ul>
                    <li>System-wide average: 98.9% (Target: 95%+)</li>
                    <li>Best performing: San Juan (99.6%)</li>
                    <li>Areas needing attention: Malabon (98.4%), Navotas (98.2%)</li>
                </ul>

                <p><strong>Risk Assessment:</strong></p>
                <ul>
                    <li>2 areas approaching minimum threshold</li>
                    <li>Recommended: Enhanced monitoring in coastal areas</li>
                    <li>Preventive action: Pipeline inspection within 90 days</li>
                </ul>

                <p><em>Analysis completed in 3.4 seconds using real-time data</em></p>
            </div>
            """, unsafe_allow_html=True)

        elif "attention" in query.lower():
            st.markdown("""
            <div style="
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Priority Analysis</h5>
                <p><strong>Areas Requiring Immediate Attention:</strong></p>

                <ol>
                    <li><strong>Malabon (98.4% quality)</strong> - Infrastructure aging</li>
                    <li><strong>Navotas (98.2% quality)</strong> - Coastal contamination risk</li>
                    <li><strong>Caloocan (High consumption growth)</strong> - Capacity constraints</li>
                </ol>

                <p><strong>Recommended Actions:</strong></p>
                <ul>
                    <li>Immediate: Enhanced water testing protocol</li>
                    <li>30 days: Pipeline inspection and maintenance</li>
                    <li>90 days: Infrastructure upgrade planning</li>
                </ul>

                <p><strong>Financial Impact:</strong> ₱850M investment vs ₱2.1B penalty risk</p>
                <p><em>Strategic analysis completed in 4.1 seconds</em></p>
            </div>
            """, unsafe_allow_html=True)

def render_ticket_classification_demo(customer_issue, customer_name, customer_area, data_processor, show_ai_fallback):
    """Render ticket classification demo"""
    with st.spinner("AI classifying customer issue..."):
        time.sleep(2)

        # Simulate AI classification based on issue content
        if "main break" in customer_issue.lower() or "flooding" in customer_issue.lower():
            priority = "Critical"
            category = "Emergency Repairs"
            confidence = 98
            assigned_tech = "Miguel Torres (Emergency Specialist)"
            eta = "15 minutes"
            solution = "Emergency crew dispatched immediately. Traffic management coordinated. Alternate supply arrangements in progress."

        elif "brown color" in customer_issue.lower() or "taste" in customer_issue.lower():
            priority = "High"
            category = "Water Quality Issues"
            confidence = 95
            assigned_tech = "Patricia Reyes (Quality Control)"
            eta = "2 hours"
            solution = "Water sampling scheduled for immediate lab analysis. System flushing may be required."

        elif "no water" in customer_issue.lower():
            priority = "Critical"
            category = "Service Interruption"
            confidence = 97
            assigned_tech = "Luis Garcia (Infrastructure)"
            eta = "30 minutes"
            solution = "Service interruption investigation initiated. Customer notification system activated."

        else:
            priority = "Medium"
            category = "General Inquiry"
            confidence = 85
            assigned_tech = "Rosa Santos (Customer Service)"
            eta = "4 hours"
            solution = "Standard troubleshooting protocol initiated. Customer follow-up scheduled."

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI Classification Results</h5>
                <p><strong>Priority:</strong> {priority}</p>
                <p><strong>Category:</strong> {category}</p>
                <p><strong>Confidence:</strong> {confidence}%</p>
                <p><strong>Ticket ID:</strong> TKT-{datetime.now().strftime('%Y%m%d')}-{hash(customer_issue) % 1000:03d}</p>
                <p><em>Classification time: 1.8 seconds</em></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            ">
                <h5>👨‍🔧 AI Technician Assignment</h5>
                <p><strong>Assigned to:</strong> {assigned_tech}</p>
                <p><strong>ETA:</strong> {eta}</p>
                <p><strong>Customer:</strong> {customer_name}</p>
                <p><strong>Area:</strong> {customer_area}</p>
                <p><em>Optimal routing calculated</em></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        ">
            <h5>💡 AI Solution Recommendation</h5>
            <p>{solution}</p>
            <p><strong>Next Steps:</strong> Customer notification sent. Technician dispatched. Monitoring activated.</p>
        </div>
        """, unsafe_allow_html=True)

def render_risk_management_view(data_processor):
    """Render risk management perspective"""
    st.markdown("""
    <div style="
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    ">
        <h4>⚠️ AI Risk Detection Dashboard</h4>
        <p>Continuous monitoring for compliance, operational, and financial risks</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🚨 Active Risk Alerts")
        st.markdown("""
        - **Medium Risk:** Malabon water quality trending down
        - **Low Risk:** Navotas pipe aging assessment due
        - **Monitor:** BGC demand capacity approaching limit
        """)

    with col2:
        st.markdown("#### 📊 Risk Categories")
        risk_data = {'Category': ['Compliance', 'Operational', 'Financial', 'Safety'], 'Count': [2, 5, 1, 0]}
        fig = px.pie(values=risk_data['Count'], names=risk_data['Category'], title="Risk Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### ⏱️ Response Times")
        st.metric("Avg Detection Time", "4.2 min", "↓ 85% improvement")
        st.metric("Mitigation Planning", "12 min", "↓ 92% improvement")
        st.metric("Stakeholder Alerts", "30 sec", "Real-time")

def render_operations_manager_view(data_processor):
    """Render operations manager perspective"""
    st.markdown("""
    <div style="
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    ">
        <h4>👨‍💼 Operations Manager Dashboard</h4>
        <p>Resource optimization and performance management</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👥 Team Performance")
        team_data = {
            'Technician': ['Miguel Torres', 'Patricia Reyes', 'Luis Garcia', 'Rosa Santos'],
            'Utilization': [85, 70, 90, 60],
            'Rating': [4.8, 4.9, 4.9, 4.5]
        }
        fig = px.scatter(x=team_data['Utilization'], y=team_data['Rating'],
                        hover_name=team_data['Technician'],
                        title="Technician Performance Matrix")
        fig.update_layout(xaxis_title="Utilization %", yaxis_title="Customer Rating")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📈 Operational Efficiency")
        st.metric("Team Utilization", "76%", "↑ 12% optimal")
        st.metric("Response Time SLA", "95%", "↑ 8% compliance")
        st.metric("Customer Satisfaction", "4.6/5", "↑ 0.3 improvement")
        st.metric("Cost per Ticket", "₱2,450", "↓ ₱890 reduction")

def render_emergency_response_view(data_processor):
    """Render emergency response perspective"""
    st.markdown("""
    <div style="
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    ">
        <h4>🚨 Emergency Response Command Center</h4>
        <p>Real-time crisis management and coordination</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🚨 Active Emergencies")
        st.markdown("""
        **CRITICAL:** Water main break - Ayala Ave
        Status: Team dispatched (ETA: 12 min)
        Impact: 1,247 customers affected

        **HIGH:** Quality alert - Malabon area
        Status: Sampling in progress
        Impact: 340 customers monitoring
        """)

    with col2:
        st.markdown("#### ⚡ Response Metrics")
        st.metric("Avg Response Time", "18 min", "↓ 27 min improvement")
        st.metric("Emergency Team Available", "3/4", "75% capacity")
        st.metric("Public Notifications", "2,847", "Auto-sent")

    with col3:
        st.markdown("#### 📊 Emergency Trends")
        emergency_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            'Emergencies': [12, 8, 15, 6, 9, 4, 7],
            'Avg Response (min)': [25, 22, 20, 18, 16, 15, 14]
        })
        fig = px.line(emergency_data, x='Month', y='Avg Response (min)',
                     title="Response Time Improvement")
        st.plotly_chart(fig, use_container_width=True)

# Update the todo status
def update_todo_status():
    """Update todo status"""
    st.session_state.setdefault('todo_status', 'completed')

# Call update at the end
update_todo_status()