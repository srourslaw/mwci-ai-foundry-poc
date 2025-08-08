import streamlit as st
import openai
import anthropic
import json
from typing import Dict, List, Any

class AIModelManager:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize AI clients with API keys"""
        try:
            if "OPENAI_API_KEY" in st.secrets:
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                self.openai_client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            if "ANTHROPIC_API_KEY" in st.secrets:
                self.anthropic_client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        except Exception as e:
            st.error(f"Error setting up AI clients: {e}")
    
    def generate_hr_response(self, user_query: str, employee_data: Dict, context: str = "") -> str:
        """Generate HR assistant response using OpenAI"""
        if not self.openai_client:
            return "AI service temporarily unavailable. Please try again later."
        
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
    
    def classify_ticket(self, ticket_description: str, categories: List[Dict]) -> Dict:
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
        """Generate insights from water data using Claude"""
        if not self.anthropic_client:
            # Fallback to OpenAI if Claude is not available
            return self.generate_data_insights_openai(query, data_context)
        
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
        """Suggest solution for ticket based on category"""
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

# Initialize global instance
@st.cache_resource
def get_ai_manager():
    return AIModelManager()