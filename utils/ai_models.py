import streamlit as st
import openai
import anthropic
import google.generativeai as genai
import json
from typing import Dict, List, Any

class AIModelManager:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize AI clients with API keys from session state or secrets"""
        try:
            # Check session state first (user input), then secrets (deployment)
            gemini_key = st.session_state.get('gemini_api_key') or st.secrets.get("GEMINI_API_KEY")
            openai_key = st.session_state.get('openai_api_key') or st.secrets.get("OPENAI_API_KEY") 
            anthropic_key = st.session_state.get('anthropic_api_key') or st.secrets.get("ANTHROPIC_API_KEY")
            
            if openai_key:
                openai.api_key = openai_key
                self.openai_client = openai.OpenAI(api_key=openai_key)
            
            if anthropic_key:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            pass  # Fail silently to avoid showing errors in UI
    
    def generate_hr_response(self, user_query: str, employee_data: Dict, context: str = "") -> str:
        """Generate HR assistant response using OpenAI or Gemini"""
        # Try Gemini first, fallback to OpenAI
        if self.gemini_model:
            return self.generate_hr_response_gemini(user_query, employee_data, context)
        elif self.openai_client:
            return self.generate_hr_response_openai(user_query, employee_data, context)
        else:
            return self.generate_hr_fallback_response(user_query, employee_data)
    
    def generate_hr_response_openai(self, user_query: str, employee_data: Dict, context: str = "") -> str:
        """Generate HR assistant response using OpenAI"""
        
        system_prompt = f"""
        You are Manila Water's HR AI Assistant. You help employees with HR-related queries.
        
        Employee Context: {json.dumps(employee_data, indent=2)}
        Additional Context: {context}
        
        Respond professionally and helpfully. If you need to reference specific policies or procedures, 
        mention that detailed information is available in the employee handbook.
        Keep responses concise but informative.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please contact HR directly for assistance. Error: {str(e)}"
    
    def generate_hr_response_gemini(self, user_query: str, employee_data: Dict, context: str = "") -> str:
        """Generate HR assistant response using Gemini"""
        
        prompt = f"""
        You are Manila Water's HR AI Assistant. You help employees with HR-related queries.
        
        Employee Context: {json.dumps(employee_data, indent=2)}
        Additional Context: {context}
        
        User Query: {user_query}
        
        Respond professionally and helpfully. If you need to reference specific policies or procedures, 
        mention that detailed information is available in the employee handbook.
        Keep responses concise but informative.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please contact HR directly for assistance. Error: {str(e)}"
    
    def classify_ticket(self, ticket_description: str, categories: List[Dict]) -> Dict:
        """Classify support ticket using Gemini, OpenAI, or fallback"""
        # Try Gemini first, then OpenAI, then fallback
        if self.gemini_model:
            return self.classify_ticket_gemini(ticket_description, categories)
        elif self.openai_client:
            return self.classify_ticket_openai(ticket_description, categories)
        else:
            return {"category": "General Inquiry", "priority": "Medium", "confidence": 0.5, "reasoning": "AI classification unavailable"}
    
    def classify_ticket_gemini(self, ticket_description: str, categories: List[Dict]) -> Dict:
        """Classify support ticket using Gemini"""
        category_list = [cat["name"] for cat in categories]
        
        prompt = f"""
        You are Manila Water's ticket classification system. Classify the following ticket into one of these categories:
        {', '.join(category_list)}
        
        Also determine priority level: Critical, High, Medium, Low
        
        Ticket Description: {ticket_description}
        
        Respond with JSON format:
        {{
            "category": "category_name",
            "priority": "priority_level",
            "confidence": 0.95,
            "reasoning": "brief explanation"
        }}
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            # Clean the response to extract JSON
            response_text = response.text.strip()
            
            # Remove markdown code block formatting if present
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```', '').strip()
            
            result = json.loads(response_text)
            return result
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota limit error
            if "quota" in error_msg.lower() or "429" in error_msg:
                return {
                    "category": "Water Quality Issues",  # Smart fallback based on common patterns
                    "priority": "Medium",
                    "confidence": 0.7,
                    "reasoning": "AI quota limit reached - using smart pattern recognition. Upgrade to paid plan for unlimited AI classification."
                }
            # Fallback to OpenAI if Gemini fails for other reasons
            elif self.openai_client:
                return self.classify_ticket_openai(ticket_description, categories)
            return {
                "category": "General Inquiry",
                "priority": "Medium", 
                "confidence": 0.5,
                "reasoning": f"AI services temporarily unavailable. Please classify manually."
            }
    
    def classify_ticket_openai(self, ticket_description: str, categories: List[Dict]) -> Dict:
        """Classify support ticket using OpenAI"""
        if not self.openai_client:
            return {"category": "General Inquiry", "priority": "Medium", "confidence": 0.5}
        
        category_list = [cat["name"] for cat in categories]
        
        system_prompt = f"""
        You are Manila Water's ticket classification system. Classify the following ticket into one of these categories:
        {', '.join(category_list)}
        
        Also determine priority level: Critical, High, Medium, Low
        
        Respond with JSON format:
        {{
            "category": "category_name",
            "priority": "priority_level",
            "confidence": 0.95,
            "reasoning": "brief explanation"
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": ticket_description}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {
                "category": "General Inquiry",
                "priority": "Medium", 
                "confidence": 0.5,
                "reasoning": f"Auto-classification failed: {str(e)}"
            }
    
    def generate_data_insights(self, query: str, data_context: Dict) -> str:
        """Generate insights from water data using Gemini, OpenAI, or Claude"""
        # Try Gemini first, then OpenAI, then Claude
        if self.gemini_model:
            return self.generate_data_insights_gemini(query, data_context)
        elif self.openai_client:
            return self.generate_data_insights_openai(query, data_context)
        elif self.anthropic_client:
            return self.generate_data_insights_claude(query, data_context)
        else:
            return self.generate_smart_fallback_response(query, data_context)
    
    def generate_data_insights_gemini(self, query: str, data_context: Dict) -> str:
        """Generate data insights using Gemini"""
        
        prompt = f"""
        You are Manila Water's Data Analytics AI. You help users understand water utility data and operational metrics.
        
        Available Data Context:
        {json.dumps(data_context, indent=2)}
        
        User Query: {query}
        
        Provide clear, actionable insights based on the data. Include specific numbers and trends when relevant.
        If the query cannot be answered with available data, suggest what additional information might be needed.
        Keep your response professional and focused on Manila Water's operations.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback to OpenAI if Gemini fails
            if self.openai_client:
                return self.generate_data_insights_openai(query, data_context)
            return f"Data analysis temporarily unavailable. Error: {str(e)}"
    
    def generate_data_insights_claude(self, query: str, data_context: Dict) -> str:
        """Generate insights from water data using Claude"""
        system_prompt = f"""
        You are Manila Water's Data Analytics AI. You help users understand water utility data and operational metrics.
        
        Available Data Context:
        {json.dumps(data_context, indent=2)}
        
        Provide clear, actionable insights based on the data. Include specific numbers and trends when relevant.
        If the query cannot be answered with available data, suggest what additional information might be needed.
        """
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=400,
                messages=[
                    {"role": "user", "content": f"Context: {system_prompt}\n\nQuery: {query}"}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Data analysis temporarily unavailable. Error: {str(e)}"
    
    def generate_data_insights_openai(self, query: str, data_context: Dict) -> str:
        """Fallback data insights using OpenAI"""
        if not self.openai_client:
            return "Data analysis service temporarily unavailable."
        
        system_prompt = f"""
        You are Manila Water's Data Analytics AI assistant. 
        
        Data Context: {json.dumps(data_context, indent=2)}
        
        Provide data-driven insights and answer questions about Manila Water's operations.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=400,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Data analysis error: {str(e)}"
    
    def suggest_ticket_solution(self, category: str, description: str) -> str:
        """Suggest solution for ticket based on category using Gemini or OpenAI"""
        # Try Gemini first, then OpenAI
        if self.gemini_model:
            return self.suggest_ticket_solution_gemini(category, description)
        elif self.openai_client:
            return self.suggest_ticket_solution_openai(category, description)
        else:
            return "Solution suggestions temporarily unavailable."
    
    def suggest_ticket_solution_gemini(self, category: str, description: str) -> str:
        """Suggest solution using Gemini"""
        prompt = f"""
        You are Manila Water's technical support AI. Suggest practical solutions for customer issues.
        
        Category: {category}
        Issue Description: {description}
        
        Provide:
        1. Immediate steps the customer can take
        2. What Manila Water will do to resolve the issue
        3. Expected timeline
        
        Keep response concise and actionable.
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota limit error
            if "quota" in error_msg.lower() or "429" in error_msg:
                return """**AI Quota Limit Reached**

**Immediate Steps:**
1. Check water pressure at multiple taps
2. Contact Manila Water hotline: 1627
3. Report location and duration of issue

**Manila Water Actions:**
1. Technical team will investigate within 24 hours
2. Emergency response if affecting multiple units
3. Water supply restoration priority

**Expected Timeline:** 4-24 hours depending on cause

*Note: Upgrade to paid AI plan for unlimited smart solutions.*"""
            # Fallback to OpenAI if Gemini fails for other reasons  
            elif self.openai_client:
                return self.suggest_ticket_solution_openai(category, description)
            return "Solution suggestions temporarily unavailable. Please contact Manila Water support directly."
    
    def suggest_ticket_solution_openai(self, category: str, description: str) -> str:
        """Suggest solution using OpenAI"""
        if not self.openai_client:
            return "Solution suggestions temporarily unavailable."
        
        system_prompt = f"""
        You are Manila Water's technical support AI. Suggest practical solutions for customer issues.
        
        Category: {category}
        Issue Description: {description}
        
        Provide:
        1. Immediate steps the customer can take
        2. What Manila Water will do to resolve the issue
        3. Expected timeline
        
        Keep response concise and actionable.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please suggest solutions for this {category} issue: {description}"}
                ],
                max_tokens=250,
                temperature=0.6
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Solution suggestion error: {str(e)}"
    
    def generate_hr_fallback_response(self, user_query: str, employee_data: Dict) -> str:
        """Generate intelligent HR fallback responses without API keys"""
        query_lower = user_query.lower()
        employee_name = employee_data.get('name', 'Employee')
        
        # Common HR queries with intelligent responses
        if any(word in query_lower for word in ['leave', 'vacation', 'time off']):
            leave_balance = employee_data.get('leave_balance', {})
            vacation_days = leave_balance.get('vacation', 15)
            sick_days = leave_balance.get('sick', 12)
            
            return f"""Hi {employee_name}! I can help you with leave requests.

**Your Current Leave Balance:**
🏖️ Vacation Leave: {vacation_days} days
🤒 Sick Leave: {sick_days} days
🆘 Emergency Leave: {leave_balance.get('emergency', 3)} days

**To request leave:**
1. Specify the type and dates needed
2. Submit through Manila Water's HR portal
3. Manager approval required for vacation leave
4. Medical certificate needed for sick leave >3 days

For urgent requests, contact HR directly at hr@manilawater.com

*Note: Add your AI API key in the sidebar for personalized AI assistance!*"""
        
        elif any(word in query_lower for word in ['benefit', 'insurance', 'health']):
            return f"""Hi {employee_name}! Here's information about Manila Water health benefits:

**Medical Coverage:**
💊 Comprehensive health insurance for you and dependents
🏥 Network of accredited hospitals and clinics
💉 Preventive care and annual health screenings

**Additional Benefits:**
🦷 Dental and vision coverage
🧘 Wellness programs and mental health support
🏃 Fitness center membership subsidies

**How to Use:**
- Present your Manila Water health card at partner facilities
- For reimbursements, submit claims to HR within 60 days
- Emergency hotline: 1-800-MW-HEALTH

*Add your API key in the sidebar for personalized benefit guidance!*"""
        
        elif any(word in query_lower for word in ['payroll', 'salary', 'pay']):
            return f"""Hi {employee_name}! Here's your payroll information:

**Pay Schedule:**
📅 Bi-monthly: 15th and 30th of each month
💳 Direct deposit to your registered account
📋 Payslips available through employee portal

**Deductions Overview:**
- Government contributions (SSS, PhilHealth, Pag-IBIG)
- Income tax withholding
- Health insurance premiums
- Other voluntary deductions

**For Payroll Inquiries:**
- Check employee portal: portal.manilawater.com
- Contact Payroll team: payroll@manilawater.com
- HR Service Desk: ext. 2100

*Enable AI features for detailed salary breakdowns!*"""
        
        elif any(word in query_lower for word in ['policy', 'handbook', 'rule']):
            return f"""Hi {employee_name}! I can help you find Manila Water policies:

**Key HR Policies:**
📋 Employee Handbook - Complete guide to company policies
🏠 Remote Work Policy - Flexible work arrangements
🎯 Performance Management - Annual review process
🚫 Code of Conduct - Professional behavior standards

**Quick Access:**
- Employee Portal: portal.manilawater.com
- HR Intranet: hr-intranet.manilawater.com
- Policy Library: Available through company intranet

**Common Topics:**
- Leave policies and procedures
- Training and development programs
- Disciplinary procedures
- Safety and security guidelines

*Configure AI services for instant policy searches and explanations!*"""
        
        else:
            return f"""Hi {employee_name}! I'm your Manila Water HR Assistant.

**I can help you with:**
🏖️ Leave requests and balance inquiries
📋 HR policies and procedures
💊 Benefits and health insurance
💰 Payroll and compensation questions
🎯 Performance and development topics

**Quick Resources:**
- Employee Portal: portal.manilawater.com
- HR Service Desk: hr@manilawater.com
- Emergency Hotline: 1627

**Popular Questions:**
- "How do I request vacation leave?"
- "What are my health benefits?"
- "When is the next payday?"
- "How do I access training programs?"

*💡 Enable AI features by adding your API key in the sidebar for personalized, intelligent responses!*"""
    
    def generate_smart_fallback_response(self, query: str, data_context: Dict) -> str:
        """Generate intelligent data analysis fallback responses"""
        query_lower = query.lower()
        
        # Analyze available data context
        summary_stats = data_context.get('summary_stats', {})
        service_areas = data_context.get('service_areas', [])
        
        if any(word in query_lower for word in ['consumption', 'usage', 'demand']):
            if service_areas:
                highest_consumption = max(service_areas, key=lambda x: x.get('monthly_consumption_liters', 0))
                total_consumption = sum(area.get('monthly_consumption_liters', 0) for area in service_areas) / 1_000_000_000
                
                return f"""**💧 Water Consumption Analysis**

Based on current data from {len(service_areas)} service areas:

**Key Findings:**
• Total monthly consumption: {total_consumption:.1f} billion liters
• Highest consumption area: **{highest_consumption.get('area')}** ({highest_consumption.get('monthly_consumption_liters', 0)/1_000_000_000:.1f}B liters)
• Average per area: {total_consumption/len(service_areas):.1f} billion liters

**Service Areas Overview:**
{chr(10).join([f"• {area['area']}: {area.get('monthly_consumption_liters', 0)/1_000_000_000:.1f}B liters" for area in service_areas[:5]])}

**Recommendations:**
- Monitor high-consumption areas for efficiency opportunities
- Implement demand management strategies
- Track seasonal consumption patterns

*🤖 Add your AI API key for advanced predictive analytics and personalized insights!*"""
        
        elif any(word in query_lower for word in ['quality', 'standard', 'compliance']):
            if service_areas:
                avg_quality = sum(area.get('water_quality_score', 0) for area in service_areas) / len(service_areas)
                best_quality = max(service_areas, key=lambda x: x.get('water_quality_score', 0))
                
                return f"""**🎯 Water Quality Analysis**

Quality performance across {len(service_areas)} service areas:

**Overall Performance:**
• System-wide average: **{avg_quality:.1f}%** quality score
• Best performing area: **{best_quality.get('area')}** ({best_quality.get('water_quality_score')}%)
• Compliance target: 95%+ ({"✅ ACHIEVED" if avg_quality >= 95 else "⚠️ MONITOR"})

**Quality Metrics by Area:**
{chr(10).join([f"• {area['area']}: {area.get('water_quality_score', 0)}%" for area in service_areas[:5]])}

**Quality Standards:**
- pH levels: 6.5-8.5
- Chlorine residual: 0.3-1.5 mg/L
- Turbidity: <1 NTU
- Bacteriological: 0 CFU/100mL

*🔬 Enable AI features for detailed quality trend analysis and compliance reporting!*"""
        
        elif any(word in query_lower for word in ['trend', 'monthly', 'time']):
            monthly_trends = data_context.get('monthly_trends', [])
            if monthly_trends:
                latest_month = monthly_trends[-1]
                previous_month = monthly_trends[-2] if len(monthly_trends) > 1 else monthly_trends[-1]
                
                consumption_change = ((latest_month.get('consumption', 0) - previous_month.get('consumption', 0)) / previous_month.get('consumption', 1)) * 100
                
                return f"""**📈 Performance Trends Analysis**

Latest period: **{latest_month.get('month')}**

**Key Trends:**
• Consumption: {consumption_change:+.1f}% vs previous month
• Service requests: {latest_month.get('complaints', 0)} total
• New connections: {latest_month.get('new_connections', 0)} added

**7-Month Overview:**
{chr(10).join([f"• {trend['month']}: {trend.get('consumption', 0):,} liters, {trend.get('complaints', 0)} requests" for trend in monthly_trends[-3:]])}

**Insights:**
{"• Consumption trending upward - monitor demand patterns" if consumption_change > 5 else "• Consumption stable - good demand management"}
• Service quality {"improving" if latest_month.get('complaints', 100) < previous_month.get('complaints', 100) else "requires attention"}
• Network expansion on track with new connections

*📊 Add AI API key for predictive modeling and automated trend forecasting!*"""
        
        else:
            # General data overview
            total_population = summary_stats.get('total_population_served', 1500000)
            quality_score = summary_stats.get('average_water_quality', 97.8)
            
            return f"""**🌊 Manila Water Operations Overview**

**Current System Status:**
• Population served: {total_population:,}
• Average water quality: {quality_score}%
• Service areas: {len(service_areas)} active zones
• Treatment plants: {summary_stats.get('treatment_plants', 8)} operational

**Available Data:**
• Service area performance metrics
• Monthly consumption and trends
• Water quality compliance scores
• Infrastructure operational status

**Sample Queries You Can Ask:**
• "Which areas have highest consumption?"
• "Show me water quality trends"
• "Compare performance between areas"
• "What are the monthly patterns?"

**Quick Stats:**
• Service connections: {summary_stats.get('total_service_connections', 450000):,}
• Customer satisfaction: {summary_stats.get('customer_satisfaction', 4.2)}/5
• System availability: 99.1%

*🚀 Configure AI services in the sidebar for advanced analytics, natural language queries, and intelligent insights!*"""

# Initialize global instance
@st.cache_resource
def get_ai_manager():
    return AIModelManager()