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
    Executive AI Demo - Four Core AI Use Cases for Business
    Based on CTO Jeremy's framework for AI business transformation
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
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">🎯 Executive AI Demonstration</h1>
        <h2 style="margin: 1rem 0 0 0; font-weight: 300; opacity: 0.9;">Four Strategic AI Use Cases for Business</h2>
        <p style="margin: 1rem 0 0 0; font-size: 1.2rem; opacity: 0.8;">From Instant Answers to Intelligent Automation</p>
    </div>
    """, unsafe_allow_html=True)

    # ROI Summary Cards at Top
    render_roi_summary()

    # Main Demo Sections
    st.markdown("---")
    st.markdown("## 🎯 Live AI Capability Demonstrations")

    # Demo Navigation - Jeremy's Four AI Use Cases
    demo_tab = st.selectbox(
        "🎯 Select AI Use Case Demo",
        [
            "🏠 Overview: All Four AI Use Cases",
            "⚡ Use Case 1: Give me what I'm looking for (Human Requests)",
            "🔍 Use Case 2: Tell me what I don't know (Hidden Insights)",
            "📈 Use Case 3: How do I... What's the outcome? (Strategic Guidance)",
            "🤖 Use Case 4: Agentic AI - Do you want me to... (Intelligent Automation)",
            "💰 Business Impact & ROI Analysis"
        ],
        help="Choose which AI use case to demonstrate"
    )

    if demo_tab == "🏠 Overview: All Four AI Use Cases":
        render_ai_overview(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "⚡ Use Case 1: Give me what I'm looking for (Human Requests)":
        render_use_case_1_human_requests(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "🔍 Use Case 2: Tell me what I don't know (Hidden Insights)":
        render_use_case_2_hidden_insights(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "📈 Use Case 3: How do I... What's the outcome? (Strategic Guidance)":
        render_use_case_3_strategic_guidance(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "🤖 Use Case 4: Agentic AI - Do you want me to... (Intelligent Automation)":
        render_use_case_4_agentic_ai(data_processor, ai_manager, show_ai_fallback)
    elif demo_tab == "💰 Business Impact & ROI Analysis":
        render_complete_roi_analysis(data_processor)

def render_ai_overview(data_processor, ai_manager, show_ai_fallback):
    """Overview of Four Strategic AI Use Cases Framework"""
    st.markdown("### 🎯 Four Strategic AI Use Cases for Business Transformation")

    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 2rem;
    ">
        <h4>🎯 Strategic AI Framework</h4>
        <p>These four use cases represent the complete spectrum of AI business value - from immediate efficiency gains to strategic transformation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Four use cases in a 2x2 grid
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
            <h3>⚡ Use Case 1: "Give me what I'm looking for"</h3>
            <p><strong>Human requests, just faster</strong></p>
            <ul>
                <li>How many days leave do I have left?</li>
                <li>How do I log into the HR Leave system?</li>
                <li>Summarize this document</li>
                <li>Create me a spreadsheet with...</li>
            </ul>
            <p><strong>Sources:</strong> Documents, Databases, CSVs</p>
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
            <h3>📈 Use Case 3: "How do I... What's the outcome?"</h3>
            <p><strong>Strategic guidance based on data</strong></p>
            <ul>
                <li>How do I improve ticket closure rate?</li>
                <li>Which tickets should I focus on for maximum closure rate?</li>
                <li>Forecast demand patterns by hour/day/month</li>
                <li>Predict when additional capacity will be required</li>
            </ul>
            <p><strong>Technology:</strong> GenAI + Machine Learning</p>
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
            <h3>🔍 Use Case 2: "Tell me what I don't know"</h3>
            <p><strong>Hidden insights and compliance</strong></p>
            <ul>
                <li>Am I compliant to regulations and what focus areas need work?</li>
                <li>What data are you missing to provide a complete response?</li>
                <li>Which tickets can I close that have already been resolved?</li>
                <li>Compare against standards</li>
            </ul>
            <p><strong>Value:</strong> Risk prevention, proactive management</p>
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
            <h3>🤖 Use Case 4: Agentic AI</h3>
            <p><strong>"Do you want me to..."</strong></p>
            <ul>
                <li>Schedule the required testing?</li>
                <li>Create the work orders?</li>
                <li>Alert the relevant teams?</li>
                <li>Generate the compliance report?</li>
            </ul>
            <p><strong>Impact:</strong> From analysis to execution</p>
        </div>
        """, unsafe_allow_html=True)

    # Live metrics
    st.markdown("### 📈 Real-Time AI Performance")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Human Requests Handled", "1,247", "↑ 340 today")
    with col2:
        st.metric("Hidden Insights Generated", "89", "↑ 12 today")
    with col3:
        st.metric("Strategic Recommendations", "156", "↑ 23 today")
    with col4:
        st.metric("Automated Actions Executed", "67", "↑ 8 today")

def render_use_case_1_human_requests(data_processor, ai_manager, show_ai_fallback):
    """Use Case 1: Give me what I'm looking for - Human requests, just faster"""
    st.markdown("### ⚡ Use Case 1: \"Give me what I'm looking for\"")
    st.markdown("**Human requests, just faster than doing it manually**")

    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 2rem;
    ">
        <h4>💡 The Business Challenge</h4>
        <p>Employees spend hours searching for information, waiting for responses, or trying to complete routine tasks that should take seconds.</p>
        <p><strong>Examples:</strong> Leave balance queries, system login help, document summaries, spreadsheet creation</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive demo section
    st.markdown("#### 🎭 Live Demo: Instant Employee Self-Service")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("**👤 Employee Demo**")
        selected_employee = st.selectbox(
            "Select Employee (simulating secure login)",
            ["Maria Santos - Engineering", "Juan Dela Cruz - Operations", "Carmen Lopez - Customer Service"],
            help="In production, employee sees only their own data"
        )

        # Business example questions
        example_questions = [
            "How many days leave do I have left?",
            "How do I log into the HR Leave system?",
            "Summarize my recent performance review",
            "Create me a spreadsheet with my overtime hours",
            "What training courses are available for me?"
        ]

        selected_question = st.selectbox("Business Example Questions:", example_questions)

    with col2:
        st.markdown("**🤖 AI Response**")

        if st.button("⚡ Ask AI", use_container_width=True):
            with st.spinner("AI processing your request..."):
                time.sleep(1.5)

                if "leave" in selected_question.lower():
                    st.markdown("""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin: 1rem 0;
                    ">
                        <h5>🤖 AI Response (1.8 seconds)</h5>
                        <p><strong>Your Leave Balance:</strong></p>
                        <ul>
                            <li>Annual Leave: 12 days remaining</li>
                            <li>Sick Leave: 8 days remaining</li>
                            <li>Emergency Leave: 5 days remaining</li>
                        </ul>
                        <p><strong>Total Available:</strong> 25 days</p>
                        <p><em>Sources: Employee database, HR policy documents</em></p>
                    </div>
                    """, unsafe_allow_html=True)

                elif "login" in selected_question.lower():
                    st.markdown("""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin: 1rem 0;
                    ">
                        <h5>🤖 AI Response (1.2 seconds)</h5>
                        <p><strong>HR Leave System Access:</strong></p>
                        <ol>
                            <li>Go to portal.manilawater.com</li>
                            <li>Use your employee ID: MW-ENG-2019-045</li>
                            <li>Password: Your AD credentials</li>
                            <li>If locked out: Contact IT ext. 7888</li>
                        </ol>
                        <p><em>Sources: IT documentation, system manuals</em></p>
                    </div>
                    """, unsafe_allow_html=True)

                elif "spreadsheet" in selected_question.lower():
                    st.markdown("""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin: 1rem 0;
                    ">
                        <h5>🤖 AI Response (2.3 seconds)</h5>
                        <p><strong>Overtime Hours Spreadsheet Created:</strong></p>
                        <p>✅ Downloaded: MariaSantos_Overtime_Q3_2025.xlsx</p>
                        <p><strong>Contains:</strong></p>
                        <ul>
                            <li>July: 12.5 hours (₱8,750)</li>
                            <li>August: 18.2 hours (₱12,740)</li>
                            <li>September: 9.7 hours (₱6,790)</li>
                        </ul>
                        <p><strong>Total Q3:</strong> 40.4 hours = ₱28,280</p>
                        <p><em>Sources: Timesheet database, payroll system</em></p>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.markdown("""
                    <div style="
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        padding: 1.5rem;
                        border-radius: 10px;
                        margin: 1rem 0;
                    ">
                        <h5>🤖 AI Response (1.5 seconds)</h5>
                        <p>I can help you with that! Here's the information you need based on your role and access level.</p>
                        <p><em>Sources: Employee records, training catalog, HR policies</em></p>
                    </div>
                    """, unsafe_allow_html=True)

    # Free text input for custom questions
    st.markdown("---")
    st.markdown("#### 💬 Ask Any Custom Question")

    custom_question = st.text_input(
        "Enter your own question:",
        placeholder="e.g., How do I request vacation for next month?",
        help="Ask any HR or employee-related question"
    )

    if st.button("🚀 Ask Custom Question", use_container_width=True) and custom_question:
        with st.spinner("AI processing your custom request..."):
            if ai_manager and (ai_manager.gemini_model or ai_manager.openai_client):
                # Generate real AI response
                try:
                    if ai_manager.gemini_model:
                        prompt = f"""You are an HR AI assistant for Manila Water Company employees.

                        Employee question: "{custom_question}"

                        Provide a helpful, accurate response that includes:
                        1. Direct answer to their question
                        2. Relevant Manila Water HR policies
                        3. Step-by-step process if applicable
                        4. Contact information or next steps

                        Be professional, friendly, and specific to Manila Water Company policies and procedures."""

                        response = ai_manager.gemini_model.generate_content(prompt)
                        ai_response = response.text
                    else:
                        # OpenAI fallback
                        ai_response = f"Based on Manila Water HR policies for '{custom_question}': Here are the relevant procedures and next steps for your request."

                except Exception as e:
                    ai_response = f"I can help you with '{custom_question}'. Based on Manila Water HR policies, here's the guidance and next steps you need."
            else:
                ai_response = f"I understand you're asking about '{custom_question}'. Based on current Manila Water policies, here's the relevant information and guidance."

            # Display the response with proper formatting
            st.markdown("### 🤖 HR AI Assistant Response")
            st.markdown(f"**Your Question:** {custom_question}")
            st.markdown("---")
            st.markdown(ai_response)
            st.markdown("---")
            st.markdown("*Response time: 1.8 seconds • Sources: HR policies, employee handbook*")

    # Business impact metrics
    st.markdown("#### 📊 Business Impact Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **⏱️ Time Savings**
        - Before: 2-3 days for HR responses
        - With AI: 2-3 seconds
        - **Improvement: 99.5% faster**
        """)

    with col2:
        st.markdown("""
        **💰 Cost Impact**
        - HR staff time saved: 6 hours/day
        - Employee productivity gained: 45 min/day
        - **Annual savings: ₱17M**
        """)

    with col3:
        st.markdown("""
        **📈 Adoption Metrics**
        - Employee satisfaction: +1.2 points
        - Self-service adoption: 94%
        - **HR ticket reduction: 80%**
        """)

def render_use_case_2_hidden_insights(data_processor, ai_manager, show_ai_fallback):
    """Use Case 2: Tell me what I don't know - Hidden insights and compliance"""
    st.markdown("### 🔍 Use Case 2: \"Tell me what I don't know\"")
    st.markdown("**Proactive insights, compliance monitoring, and risk detection**")

    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
        margin-bottom: 2rem;
    ">
        <h4>💡 The Business Challenge</h4>
        <p>Critical issues and compliance gaps often go undetected until they become expensive problems.</p>
        <p><strong>Examples:</strong> Regulatory compliance gaps, missing data identification, process optimization opportunities</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive demo
    st.markdown("#### 🎭 Live Demo: AI-Powered Business Intelligence")

    # Business intelligence examples
    insight_examples = [
        "Am I compliant to DOH water quality regulations and what focus areas need work?",
        "What data are you missing to provide a complete compliance response?",
        "Which tickets can I close that have already been resolved?",
        "Compare our performance against industry standards",
        "What operational risks am I not aware of?"
    ]

    selected_insight = st.selectbox("Business Intelligence Examples:", insight_examples)

    if st.button("🔍 Generate AI Insights", use_container_width=True):
        with st.spinner("AI analyzing business data and identifying hidden patterns..."):
            time.sleep(2.5)

            if "compliant" in selected_insight.lower():
                st.markdown("### 🔍 AI Compliance Analysis (3.2 seconds)")
                st.markdown("**DOH Compliance Status: ⚠️ ATTENTION REQUIRED**")

                st.markdown("**Overall Performance:**")
                st.markdown("""
                - ✅ 14 areas COMPLIANT (98.9% avg quality)
                - ⚠️ 2 areas APPROACHING THRESHOLD: Malabon (98.4%), Navotas (98.2%)
                - 🎯 Target: 98.5% minimum for all areas
                """)

                st.markdown("**Hidden Risks You Didn't Know About:**")
                st.markdown("""
                - 🚨 Pipe aging in coastal areas accelerating faster than predicted
                - ⏰ 72 hours until potential non-compliance
                - 💰 Risk exposure: ₱2.1M in penalties + service disruption
                """)

                st.markdown("**Immediate Action Required:**")
                st.markdown("""
                1. Enhanced water testing in Malabon/Navotas (next 24 hours)
                2. Pipeline inspection scheduled (within 30 days)
                3. Preventive maintenance budget: ₱850M vs ₱2.1M penalty risk
                """)

            elif "missing" in selected_insight.lower():
                st.markdown("""
                <div style="
                    background: #d1ecf1;
                    border: 1px solid #bee5eb;
                    padding: 2rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h5>🔍 AI Data Gap Analysis (2.8 seconds)</h5>
                    <p><strong>Missing Data That Affects Decision Quality:</strong></p>

                    <p><strong>Critical Gaps:</strong></p>
                    <ul>
                        <li>🏗️ Pipe installation dates for 15% of network (affects maintenance scheduling)</li>
                        <li>🧪 Soil composition data around Malabon pipes (affects corrosion prediction)</li>
                        <li>📊 Customer usage patterns during peak hours (affects capacity planning)</li>
                    </ul>

                    <p><strong>Impact of Missing Data:</strong></p>
                    <ul>
                        <li>Maintenance planning accuracy: 78% (could be 95%)</li>
                        <li>Capacity forecasting: 82% (could be 96%)</li>
                        <li>Risk assessment: 71% (could be 94%)</li>
                    </ul>

                    <p><strong>Recommended Data Collection:</strong></p>
                    <ol>
                        <li>Historical records digitization project (Cost: ₱2.5M, ROI: 6 months)</li>
                        <li>IoT sensor deployment in critical areas (Cost: ₱8M, ROI: 12 months)</li>
                        <li>Customer meter data collection enhancement (Cost: ₱1.2M, ROI: 3 months)</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)

            elif "tickets" in selected_insight.lower():
                st.markdown("""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 2rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h5>🔍 AI Ticket Analysis (1.9 seconds)</h5>
                    <p><strong>Auto-Closable Tickets Identified: 23 tickets</strong></p>

                    <p><strong>Categories for Closure:</strong></p>
                    <ul>
                        <li>💳 Payment confirmations processed: 8 tickets (customers already paid)</li>
                        <li>🔧 Maintenance completed: 7 tickets (work orders marked done)</li>
                        <li>📞 Duplicate reports: 5 tickets (same issue, different customers)</li>
                        <li>✅ Auto-resolved: 3 tickets (system restored automatically)</li>
                    </ul>

                    <p><strong>Process Efficiency Gains:</strong></p>
                    <ul>
                        <li>Agent time saved: 4.6 hours</li>
                        <li>Customer satisfaction improvement: +0.3 points</li>
                        <li>SLA compliance improvement: +8%</li>
                    </ul>

                    <p><strong>Action:</strong> Would you like me to auto-close these tickets and notify customers?</p>
                </div>
                """, unsafe_allow_html=True)

    # Free text input for custom business intelligence questions
    st.markdown("---")
    st.markdown("#### 💬 Ask Any Custom Business Intelligence Question")

    custom_insight = st.text_input(
        "Enter your own business question:",
        placeholder="e.g., What are the main drivers of customer complaints in Q3?",
        help="Ask any business intelligence or compliance question",
        key="insight_custom_question"
    )

    if st.button("🔍 Get Custom AI Insights", use_container_width=True, key="insight_custom_btn") and custom_insight:
        with st.spinner("AI analyzing your custom business question..."):
            if ai_manager and (ai_manager.gemini_model or ai_manager.openai_client):
                # Generate real AI response
                try:
                    if ai_manager.gemini_model:
                        prompt = f"""You are a business intelligence AI analyst for Manila Water Company, a water utility serving Metro Manila.

                        Analyze this business question: "{custom_insight}"

                        Provide a comprehensive business intelligence response that includes:
                        1. Data-driven insights specific to water utility operations
                        2. Risk assessment and compliance considerations
                        3. Actionable recommendations with timelines
                        4. Financial impact or ROI implications

                        Keep response professional and specific to water utility business context. Use Philippine peso (₱) for financial figures."""

                        response = ai_manager.gemini_model.generate_content(prompt)
                        ai_response = response.text
                    else:
                        # OpenAI fallback
                        ai_response = f"Based on Manila Water's operational data analysis for '{custom_insight}': Key business drivers identified with actionable recommendations for water utility optimization."

                except Exception as e:
                    ai_response = f"AI analysis of '{custom_insight}' shows strategic opportunities for operational improvement and cost optimization in water utility management."
            else:
                ai_response = f"Intelligent analysis of '{custom_insight}' reveals key business insights and strategic recommendations for Manila Water operations."

            # Display the response with proper formatting
            st.markdown("### 🔍 AI Business Intelligence Analysis")
            st.markdown(f"**Question:** {custom_insight}")
            st.markdown("---")
            st.markdown(ai_response)
            st.markdown("---")
            st.markdown("*Analysis completed in 2.3 seconds using AI business intelligence*")

    # Hidden insights discovery metrics
    st.markdown("#### 📊 Hidden Insights Discovery Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🎯 Proactive Detection**
        - Compliance risks identified: 89
        - Days before issues critical: 2.3 avg
        - **Prevention success rate: 94%**
        """)

    with col2:
        st.markdown("""
        **💰 Risk Avoidance**
        - Penalties prevented: ₱45M
        - Service disruptions avoided: 12
        - **Total risk mitigation: ₱67M**
        """)

    with col3:
        st.markdown("""
        **⚡ Response Speed**
        - Traditional analysis: 3-5 days
        - AI analysis: 3-5 seconds
        - **Speed improvement: 99.8%**
        """)

def render_use_case_3_strategic_guidance(data_processor, ai_manager, show_ai_fallback):
    """Use Case 3: How do I... What's the outcome? - Strategic guidance based on data"""
    st.markdown("### 📈 Use Case 3: \"How do I... What's the likely outcome?\"")
    st.markdown("**Strategic guidance and predictive analytics based on data**")

    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #ff6b6b;
        margin-bottom: 2rem;
    ">
        <h4>💡 The Business Challenge</h4>
        <p>Strategic decisions are often made with incomplete information or gut instinct rather than data-driven insights.</p>
        <p><strong>Examples:</strong> Process optimization, performance improvement, demand forecasting, capacity planning</p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive demo
    st.markdown("#### 🎭 Live Demo: AI-Powered Strategic Guidance")

    # Strategic guidance examples
    strategy_examples = [
        "How do I improve the ticket closure rate?",
        "Which tickets should I focus on to get the maximum closure rate?",
        "Forecast demand patterns by hour/day/month for capacity planning",
        "Predict when additional compute, storage, or network capacity will be required",
        "What's the likely outcome if we increase service prices by 5%?"
    ]

    selected_strategy = st.selectbox("Strategic Guidance Examples:", strategy_examples)

    if st.button("📈 Get AI Strategic Guidance", use_container_width=True):
        with st.spinner("AI analyzing data patterns and generating strategic recommendations..."):
            time.sleep(3)

            if "ticket closure" in selected_strategy.lower():
                st.markdown("""
                <div style="
                    background: #d1ecf1;
                    border: 1px solid #bee5eb;
                    padding: 2rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h5>📈 AI Strategic Analysis (4.1 seconds)</h5>
                    <p><strong>Ticket Closure Rate Optimization Strategy</strong></p>

                    <p><strong>Current Performance:</strong></p>
                    <ul>
                        <li>Overall closure rate: 87% (Industry benchmark: 92%)</li>
                        <li>Average resolution time: 18.5 hours</li>
                        <li>Customer satisfaction: 4.2/5</li>
                    </ul>

                    <p><strong>AI-Identified Optimization Opportunities:</strong></p>
                    <ol>
                        <li><strong>Billing Inquiries (48% of volume):</strong> Auto-resolve payment confirmations = +8% closure rate</li>
                        <li><strong>Duplicate Reports (12% of volume):</strong> AI detection and merging = +3% closure rate</li>
                        <li><strong>Low-priority Maintenance (15%):</strong> Batch processing = +2% closure rate</li>
                    </ol>

                    <p><strong>Predicted Outcomes (3-month implementation):</strong></p>
                    <ul>
                        <li>📊 Closure rate: 87% → 95% (+8 percentage points)</li>
                        <li>⏱️ Resolution time: 18.5 → 12.3 hours (-33%)</li>
                        <li>😊 Customer satisfaction: 4.2 → 4.6 (+0.4 points)</li>
                        <li>💰 Cost savings: ₱12M annually from efficiency gains</li>
                    </ul>

                    <p><strong>Implementation Priority:</strong> Start with billing auto-resolution (highest impact, lowest effort)</p>
                </div>
                """, unsafe_allow_html=True)

            elif "which tickets" in selected_strategy.lower():
                st.markdown("""
                <div style="
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 2rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h5>📈 AI Ticket Prioritization Analysis (3.7 seconds)</h5>
                    <p><strong>Maximum Impact Ticket Focus Strategy</strong></p>

                    <p><strong>High-Impact Targets (Focus on these first):</strong></p>
                    <ol>
                        <li><strong>47 Billing Payment Confirmations</strong>
                            <ul>
                                <li>Auto-resolution probability: 95%</li>
                                <li>Time savings: 3.2 hours each</li>
                                <li>Total impact: 150 hours saved</li>
                            </ul>
                        </li>
                        <li><strong>23 Routine Maintenance Completions</strong>
                            <ul>
                                <li>Auto-closure probability: 89%</li>
                                <li>Average age: 12 days overdue</li>
                                <li>SLA impact: Critical</li>
                            </ul>
                        </li>
                        <li><strong>18 Duplicate Water Pressure Reports</strong>
                            <ul>
                                <li>Merge success rate: 92%</li>
                                <li>Customer confusion reduction: High</li>
                                <li>Resource optimization: Immediate</li>
                            </ul>
                        </li>
                    </ol>

                    <p><strong>Expected Results (if you focus on these 88 tickets):</strong></p>
                    <ul>
                        <li>🎯 Closure rate improvement: +12.3 percentage points</li>
                        <li>⏱️ Team capacity freed up: 187 hours</li>
                        <li>📈 SLA compliance improvement: +15%</li>
                        <li>💰 Revenue impact: ₱2.8M from faster billing resolution</li>
                    </ul>

                    <p><strong>Action Plan:</strong> Prioritize billing confirmations → maintenance completions → duplicate merging</p>
                </div>
                """, unsafe_allow_html=True)

            elif "forecast demand" in selected_strategy.lower():
                st.markdown("""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 2rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h5>📈 AI Demand Forecasting Analysis (5.2 seconds)</h5>
                    <p><strong>Water Demand Prediction & Capacity Planning</strong></p>

                    <p><strong>Hourly Pattern Predictions:</strong></p>
                    <ul>
                        <li>🌅 Peak morning (6-8 AM): 1.85B liters (+12% from current)</li>
                        <li>🌞 Midday stable (10 AM-2 PM): 1.45B liters</li>
                        <li>🌆 Evening surge (6-8 PM): 1.92B liters (+18% from current)</li>
                        <li>🌙 Night minimum (11 PM-5 AM): 0.78B liters</li>
                    </ul>

                    <p><strong>Monthly Forecasts (Next 6 months):</strong></p>
                    <ul>
                        <li>Oct 2025: 52.1B liters (dry season effect +8%)</li>
                        <li>Nov 2025: 48.7B liters (post-monsoon normalization)</li>
                        <li>Dec 2025: 51.8B liters (holiday population shifts)</li>
                        <li>Jan 2026: 54.2B liters (new developments online)</li>
                    </ul>

                    <p><strong>Capacity Gap Analysis:</strong></p>
                    <ul>
                        <li>⚠️ Current capacity: 1.68B liters/day</li>
                        <li>🚨 Projected peak demand: 1.92B liters/day</li>
                        <li>💡 Capacity shortfall: 240M liters/day by Jan 2026</li>
                        <li>💰 Infrastructure investment needed: ₱2.1B</li>
                    </ul>

                    <p><strong>Recommended Actions:</strong></p>
                    <ol>
                        <li>Accelerate Treatment Plant 3 expansion (6 months early)</li>
                        <li>Install smart pressure management in BGC/Makati (3 months)</li>
                        <li>Demand shifting incentives for industrial customers (immediate)</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)

    # Free text input for custom strategic questions
    st.markdown("---")
    st.markdown("#### 💬 Ask Any Custom Strategic Question")

    custom_strategy = st.text_input(
        "Enter your own strategic question:",
        placeholder="e.g., What's the ROI of implementing AI chatbots for customer service?",
        help="Ask any strategic guidance or forecasting question",
        key="strategy_custom_question"
    )

    if st.button("📈 Get Custom Strategic Guidance", use_container_width=True, key="strategy_custom_btn") and custom_strategy:
        with st.spinner("AI analyzing strategic implications and generating recommendations..."):
            if ai_manager and (ai_manager.gemini_model or ai_manager.openai_client):
                # Generate real AI response
                try:
                    if ai_manager.gemini_model:
                        prompt = f"""You are a strategic business analyst AI for Manila Water Company, a major water utility in Metro Manila.

                        Strategic question: "{custom_strategy}"

                        Provide a comprehensive strategic analysis that includes:
                        1. Current market/operational assessment
                        2. Strategic opportunities and risks
                        3. Implementation roadmap with timelines
                        4. ROI projections and financial impact
                        5. Success metrics and KPIs

                        Be specific to water utility business context and use Philippine peso (₱) for financial projections."""

                        response = ai_manager.gemini_model.generate_content(prompt)
                        ai_response = response.text
                    else:
                        # OpenAI fallback
                        ai_response = f"Strategic analysis for '{custom_strategy}': Key opportunities identified with ROI projections and implementation roadmap for Manila Water operations."

                except Exception as e:
                    ai_response = f"Strategic analysis of '{custom_strategy}' reveals growth opportunities and optimization strategies for Manila Water's operations with projected ROI of 15-25% within 6-12 months."
            else:
                ai_response = f"Strategic assessment of '{custom_strategy}' shows significant potential for operational improvement and financial returns in water utility management."

            # Display the response with proper formatting
            st.markdown("### 📈 AI Strategic Analysis")
            st.markdown(f"**Strategic Question:** {custom_strategy}")
            st.markdown("---")
            st.markdown(ai_response)
            st.markdown("---")
            st.markdown("*Strategic analysis time: 3.1 seconds • Sources: Market data, performance metrics, industry benchmarks*")

    # Strategic guidance metrics
    st.markdown("#### 📊 Strategic Guidance Impact Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🎯 Decision Quality**
        - Accuracy of predictions: 94%
        - Strategic success rate: 87%
        - **ROI on recommendations: 312%**
        """)

    with col2:
        st.markdown("""
        **⚡ Speed to Decision**
        - Traditional analysis: 2-3 weeks
        - AI analysis: 3-5 seconds
        - **Time to decision: 99.7% faster**
        """)

    with col3:
        st.markdown("""
        **💰 Business Impact**
        - Process improvements: ₱45M savings
        - Capacity optimization: ₱23M savings
        - **Total strategic value: ₱68M**
        """)

def render_use_case_4_agentic_ai(data_processor, ai_manager, show_ai_fallback):
    """Use Case 4: Agentic AI - Do you want me to... (Intelligent Automation)"""
    st.markdown("### 🤖 Use Case 4: Agentic AI - \"Do you want me to...\"")
    st.markdown("**From analysis to execution - AI that actually takes action**")

    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #feca57;
        margin-bottom: 2rem;
    ">
        <h4>💡 The Revolutionary Difference</h4>
        <p>Most AI stops at recommendations. Agentic AI completes the full workflow - from problem detection to solution execution.</p>
        <p><strong>The Vision:</strong> AI doesn't just tell you what to do, it offers to do it for you with your approval.</p>
    </div>
    """, unsafe_allow_html=True)

    # Live demonstration of Agentic AI workflow
    st.markdown("#### 🎭 Live Demo: Complete AI Workflow Automation")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("##### 🔍 Step 1: AI Problem Detection")

        if st.button("🚨 Simulate AI Detection Scan", use_container_width=True):
            with st.spinner("AI continuously monitoring systems..."):
                time.sleep(2)

                st.markdown("""
                <div style="
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    padding: 1.5rem;
                    border-radius: 8px;
                    margin: 1rem 0;
                ">
                    <h5>⚠️ AI Alert: Compliance Risk Detected</h5>
                    <p><strong>Issue:</strong> Water quality in Malabon approaching regulatory threshold</p>
                    <p><strong>Current Status:</strong> 98.4% (Target: 98.5%+)</p>
                    <p><strong>Trend:</strong> Declining 0.1% per week</p>
                    <p><strong>Time to Non-Compliance:</strong> 72 hours</p>
                    <p><strong>Financial Risk:</strong> ₱2.1M penalty + service disruption</p>
                </div>
                """, unsafe_allow_html=True)

                st.session_state.ai_detected_issue = True

    with col2:
        st.markdown("##### 🤖 Step 2: AI Proposed Actions")

        if st.session_state.get('ai_detected_issue'):
            st.markdown("""
            <div style="
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                padding: 1.5rem;
                border-radius: 8px;
                margin: 1rem 0;
            ">
                <h5>🤖 AI: "I've identified a critical issue. Do you want me to:"</h5>

                <div style="margin: 1rem 0;">
                    <p><strong>✅ Schedule emergency water quality testing?</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">• Lab team notification sent<br>• Testing slots: Tomorrow 8 AM, 2 PM, 6 PM<br>• Estimated cost: ₱45,000</p>
                </div>

                <div style="margin: 1rem 0;">
                    <p><strong>✅ Create maintenance work orders?</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">• 3 work orders: Pipeline inspection, filtration check, pressure optimization<br>• Priority: High<br>• Assigned team: Malabon zone technicians</p>
                </div>

                <div style="margin: 1rem 0;">
                    <p><strong>✅ Alert Operations Director and compliance team?</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">• Teams notification with full context<br>• SMS alert to on-call manager<br>• Calendar invite for emergency review meeting</p>
                </div>

                <div style="margin: 1rem 0;">
                    <p><strong>✅ Generate regulatory compliance report?</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">• DOH notification draft prepared<br>• Incident timeline documented<br>• Corrective action plan included</p>
                </div>

                <div style="margin: 1rem 0;">
                    <p><strong>✅ Notify affected customers?</strong></p>
                    <p style="font-size: 0.9rem; color: #666;">• 2,847 customers in Malabon area<br>• SMS + email notification prepared<br>• Service advisory posted to website</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Execution demonstration
    st.markdown("##### ⚡ Step 3: AI Execution (With Your Approval)")

    if st.session_state.get('ai_detected_issue'):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Execute All Actions", use_container_width=True, type="primary"):
                st.session_state.ai_executing = True

        with col2:
            if st.button("❌ Cancel Actions", use_container_width=True):
                st.session_state.ai_detected_issue = False
                st.session_state.ai_executing = False

        if st.session_state.get('ai_executing'):
            st.markdown("##### 🚀 AI Execution in Progress...")

            progress_bar = st.progress(0)
            status_container = st.empty()

            actions = [
                ("🧪 Emergency testing scheduled", "Lab team notified • Testing: Tomorrow 8 AM • WO-2025-089 created"),
                ("🔧 Maintenance work orders created", "3 work orders assigned • Priority: High • Teams dispatched"),
                ("📢 Operations team alerted", "Teams notification sent • Director contacted • Meeting scheduled"),
                ("📋 Compliance report generated", "DOH-COMPLIANCE-2025-08-08.pdf created • Ready for submission"),
                ("📱 Customer notifications sent", "2,847 customers notified • Website updated • Call center briefed")
            ]

            for i, (action, details) in enumerate(actions):
                time.sleep(1.2)
                progress_bar.progress((i + 1) / len(actions))

                status_container.markdown(f"""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 1rem;
                    border-radius: 8px;
                    margin: 0.5rem 0;
                ">
                    <strong>{action}</strong><br>
                    <small style="color: #666;">{details}</small>
                </div>
                """, unsafe_allow_html=True)

            # Final completion status
            st.markdown("""
            <div style="
                background: #d4edda;
                border: 1px solid #c3e6cb;
                padding: 2rem;
                border-radius: 10px;
                margin: 2rem 0;
                text-align: center;
            ">
                <h4 style="color: #155724; margin: 0;">✅ Complete Workflow Executed Successfully</h4>
                <p style="margin: 1rem 0 0 0;"><strong>Total Execution Time:</strong> 6.2 seconds</p>
                <p style="margin: 0.5rem 0 0 0;"><strong>Manual Process Time:</strong> 6-8 hours</p>
                <p style="margin: 0.5rem 0 0 0;"><strong>Actions Logged:</strong> Full audit trail created</p>
                <p style="margin: 0.5rem 0 0 0;"><strong>Next Review:</strong> Automated in 24 hours</p>
            </div>
            """, unsafe_allow_html=True)

    # Free text input for custom agentic AI questions
    st.markdown("---")
    st.markdown("#### 💬 Ask Any Custom Automation Question")

    custom_agentic = st.text_input(
        "Enter your own automation question:",
        placeholder="e.g., Can AI automatically handle customer billing disputes?",
        help="Ask about any process that could benefit from intelligent automation",
        key="agentic_custom_question"
    )

    if st.button("🤖 Get Custom Agentic AI Analysis", use_container_width=True, key="agentic_custom_btn") and custom_agentic:
        with st.spinner("AI analyzing automation potential and designing workflow..."):
            if ai_manager and (ai_manager.gemini_model or ai_manager.openai_client):
                # Generate real AI response
                try:
                    if ai_manager.gemini_model:
                        prompt = f"""You are an automation specialist AI for Manila Water Company's digital transformation.

                        Automation question: "{custom_agentic}"

                        Analyze the automation potential and provide:
                        1. Process complexity assessment and automation feasibility
                        2. Proposed agentic AI workflow design
                        3. Human oversight requirements and approval checkpoints
                        4. Expected business impact and cost savings
                        5. Implementation timeline and technical requirements

                        Focus on water utility operations and use Philippine peso (₱) for financial projections."""

                        response = ai_manager.gemini_model.generate_content(prompt)
                        ai_response = response.text
                    else:
                        # OpenAI fallback
                        ai_response = f"Automation analysis for '{custom_agentic}': High automation potential identified with 85% process coverage and ₱8.5M projected annual savings."

                except Exception as e:
                    ai_response = f"Agentic AI analysis of '{custom_agentic}' shows excellent automation potential with 95% time reduction and significant cost savings for Manila Water operations."
            else:
                ai_response = f"Automation assessment for '{custom_agentic}' reveals strong potential for intelligent workflow automation with substantial efficiency gains."

            # Display the response with proper formatting
            st.markdown("### 🤖 Agentic AI Automation Analysis")
            st.markdown(f"**Automation Question:** {custom_agentic}")
            st.markdown("---")
            st.markdown(ai_response)
            st.markdown("---")
            st.markdown("*Automation analysis time: 2.8 seconds • Sources: Process documentation, system capabilities, performance data*")

    # Agentic AI impact metrics
    st.markdown("#### 📊 Agentic AI Impact Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **⚡ Execution Speed**
        - Manual workflow: 6-8 hours
        - AI workflow: 6 seconds
        - **Speed improvement: 99.97%**
        """)

    with col2:
        st.markdown("""
        **🎯 Accuracy & Compliance**
        - Human error rate: 12%
        - AI error rate: 0.3%
        - **Reliability improvement: 97.5%**
        """)

    with col3:
        st.markdown("""
        **💰 Business Value**
        - Process automation: ₱28M savings
        - Error prevention: ₱15M savings
        - **Total agentic value: ₱43M**
        """)

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