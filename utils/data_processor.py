import json
import pandas as pd
import streamlit as st
from typing import Dict, List, Any
import os

class DataProcessor:
    def __init__(self):
        self.data_cache = {}
        self.load_all_data()
    
    def load_json_file(self, filepath: str) -> Dict:
        """Load JSON file with error handling"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            st.error(f"Data file not found: {filepath}")
            return {}
        except json.JSONDecodeError:
            st.error(f"Invalid JSON format in: {filepath}")
            return {}
    
    def load_all_data(self):
        """Load all data files into cache"""
        data_files = {
            'employees': 'data/employees.json',
            'tickets': 'data/tickets.json',
            'water_data': 'data/water_data.json',
            'policies': 'data/policies.json'
        }
        
        for key, filepath in data_files.items():
            self.data_cache[key] = self.load_json_file(filepath)
    
    # Employee Data Methods
    def get_employee_by_id(self, emp_id: str) -> Dict:
        """Get employee data by ID"""
        employees = self.data_cache.get('employees', {}).get('employees', [])
        for emp in employees:
            if emp['id'] == emp_id:
                return emp
        return {}
    
    def get_employee_by_name(self, name: str) -> Dict:
        """Get employee data by name"""
        employees = self.data_cache.get('employees', {}).get('employees', [])
        for emp in employees:
            if emp['name'].lower() == name.lower():
                return emp
        return {}
    
    def get_all_employees(self) -> List[Dict]:
        """Get all employees"""
        return self.data_cache.get('employees', {}).get('employees', [])
    
    def get_departments(self) -> List[str]:
        """Get all departments"""
        return self.data_cache.get('employees', {}).get('departments', [])
    
    def get_leave_policies(self) -> Dict:
        """Get leave policies"""
        return self.data_cache.get('employees', {}).get('leave_policies', {})
    
    # HR Policy Methods
    def get_hr_policies(self) -> Dict:
        """Get all HR policies"""
        return self.data_cache.get('policies', {}).get('hr_policies', {})
    
    def get_policy_by_name(self, policy_name: str) -> Dict:
        """Get specific policy by name"""
        policies = self.get_hr_policies()
        return policies.get(policy_name, {})
    
    def get_onboarding_faq(self) -> List[Dict]:
        """Get onboarding FAQ"""
        return self.data_cache.get('policies', {}).get('onboarding_faq', [])
    
    def search_faq(self, query: str) -> List[Dict]:
        """Search FAQ by query"""
        faq = self.get_onboarding_faq()
        results = []
        query_lower = query.lower()
        
        for item in faq:
            if (query_lower in item.get('question', '').lower() or 
                query_lower in item.get('answer', '').lower()):
                results.append(item)
        return results
    
    # Ticket Data Methods
    def get_ticket_categories(self) -> List[Dict]:
        """Get all ticket categories"""
        return self.data_cache.get('tickets', {}).get('ticket_categories', [])
    
    def get_technicians(self) -> List[Dict]:
        """Get all technicians"""
        return self.data_cache.get('tickets', {}).get('technicians', [])
    
    def get_available_technicians(self) -> List[Dict]:
        """Get available technicians"""
        techs = self.get_technicians()
        return [tech for tech in techs if tech.get('status') == 'Available']
    
    def find_best_technician(self, category: str, area: str = None) -> Dict:
        """Find best technician for a category and area"""
        techs = self.get_available_technicians()
        
        # Simple matching logic - can be enhanced with ML
        for tech in techs:
            if category.lower() in tech.get('specialty', '').lower():
                if area and area.lower() in tech.get('zone', '').lower():
                    return tech
        
        # Fallback to any available technician
        return techs[0] if techs else {}
    
    def get_sample_tickets(self) -> List[Dict]:
        """Get sample tickets"""
        return self.data_cache.get('tickets', {}).get('sample_tickets', [])
    
    # Water Data Methods
    def get_service_areas(self) -> List[Dict]:
        """Get all service areas"""
        return self.data_cache.get('water_data', {}).get('service_areas', [])
    
    def get_area_data(self, area_name: str) -> Dict:
        """Get data for specific area"""
        areas = self.get_service_areas()
        for area in areas:
            if area.get('area', '').lower() == area_name.lower():
                return area
        return {}
    
    def get_operational_metrics(self) -> Dict:
        """Get operational metrics"""
        return self.data_cache.get('water_data', {}).get('operational_metrics', {})
    
    def get_monthly_trends(self) -> List[Dict]:
        """Get monthly trends data"""
        return self.data_cache.get('water_data', {}).get('monthly_trends', [])
    
    def get_water_quality_params(self) -> Dict:
        """Get water quality parameters"""
        return self.data_cache.get('water_data', {}).get('water_quality_parameters', {})
    
    def get_infrastructure_status(self) -> Dict:
        """Get infrastructure status"""
        return self.data_cache.get('water_data', {}).get('infrastructure_status', {})
    
    # Analytics Methods
    def calculate_total_consumption(self) -> float:
        """Calculate total monthly consumption across all areas"""
        areas = self.get_service_areas()
        total = sum(area.get('monthly_consumption_liters', 0) for area in areas)
        return total / 1_000_000_000  # Convert to billion liters
    
    def calculate_average_quality_score(self) -> float:
        """Calculate average water quality score"""
        areas = self.get_service_areas()
        if not areas:
            return 0
        total_score = sum(area.get('water_quality_score', 0) for area in areas)
        return total_score / len(areas)
    
    def get_top_consuming_areas(self, limit: int = 3) -> List[Dict]:
        """Get top consuming areas"""
        areas = self.get_service_areas()
        sorted_areas = sorted(areas, 
                            key=lambda x: x.get('monthly_consumption_liters', 0), 
                            reverse=True)
        return sorted_areas[:limit]
    
    def get_trends_dataframe(self) -> pd.DataFrame:
        """Get monthly trends as DataFrame for plotting"""
        trends = self.get_monthly_trends()
        return pd.DataFrame(trends)
    
    def get_areas_dataframe(self) -> pd.DataFrame:
        """Get service areas as DataFrame"""
        areas = self.get_service_areas()
        return pd.DataFrame(areas)
    
    # Search and Filter Methods
    def search_employees(self, query: str) -> List[Dict]:
        """Search employees by name or department"""
        employees = self.get_all_employees()
        results = []
        query_lower = query.lower()
        
        for emp in employees:
            if (query_lower in emp.get('name', '').lower() or
                query_lower in emp.get('department', '').lower() or
                query_lower in emp.get('position', '').lower()):
                results.append(emp)
        return results
    
    def filter_areas_by_quality(self, min_score: float = 99.0) -> List[Dict]:
        """Filter areas by minimum quality score"""
        areas = self.get_service_areas()
        return [area for area in areas 
                if area.get('water_quality_score', 0) >= min_score]
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics for dashboard"""
        areas = self.get_service_areas()
        metrics = self.get_operational_metrics()
        
        total_population = sum(area.get('population', 0) for area in areas)
        total_connections = sum(area.get('service_connections', 0) for area in areas)
        avg_quality = self.calculate_average_quality_score()
        total_consumption = self.calculate_total_consumption()
        
        return {
            'total_population_served': total_population,
            'total_service_connections': total_connections,
            'average_water_quality': round(avg_quality, 1),
            'monthly_consumption_billion_liters': round(total_consumption, 1),
            'treatment_plants': metrics.get('total_treatment_plants', 0),
            'pipeline_network_km': metrics.get('total_pipeline_km', 0),
            'customer_satisfaction': metrics.get('customer_satisfaction_score', 0),
            'average_response_time': metrics.get('average_response_time_hours', 0)
        }

# Initialize global instance
@st.cache_resource
def get_data_processor():
    return DataProcessor()