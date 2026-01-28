#!/usr/bin/env python3
"""
Fire Department Analytics Engine
Processes data and generates insights
"""
import json
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

class FireDeptAnalytics:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Use relative path from python-engine directory
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, '..', 'data')
        self.data_dir = data_dir
        self.load_data()
    
    def load_data(self):
        """Load all data files"""
        with open(f"{self.data_dir}/incidents.json") as f:
            self.incidents = json.load(f)
        
        with open(f"{self.data_dir}/vendors.json") as f:
            self.vendors = json.load(f)
        
        with open(f"{self.data_dir}/vendor_deliveries.json") as f:
            self.deliveries = json.load(f)
        
        with open(f"{self.data_dir}/fire_stations.json") as f:
            self.stations = json.load(f)
        
        # Convert to DataFrames for analysis
        self.df_incidents = pd.DataFrame(self.incidents)
        self.df_incidents['timestamp'] = pd.to_datetime(self.df_incidents['timestamp'])
        
        self.df_vendors = pd.DataFrame(self.vendors)
        self.df_deliveries = pd.DataFrame(self.deliveries)
        self.df_stations = pd.DataFrame(self.stations)
    
    def get_dashboard_kpis(self):
        """Calculate KPIs for executive dashboard"""
        total_incidents = len(self.incidents)
        
        avg_response_time = round(
            sum(i['response_time_minutes'] for i in self.incidents) / total_incidents, 2
        )
        
        total_casualties = sum(i['casualties'] for i in self.incidents)
        total_injuries = sum(i['injuries'] for i in self.incidents)
        
        # Recent incidents (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_incidents = [
            i for i in self.incidents 
            if datetime.fromisoformat(i['timestamp']) > thirty_days_ago
        ]
        
        # Calculate trends
        sixty_days_ago = datetime.now() - timedelta(days=60)
        previous_month_incidents = [
            i for i in self.incidents 
            if sixty_days_ago < datetime.fromisoformat(i['timestamp']) <= thirty_days_ago
        ]
        
        incident_trend = len(recent_incidents) - len(previous_month_incidents)
        
        return {
            "total_incidents": total_incidents,
            "recent_incidents_30d": len(recent_incidents),
            "avg_response_time": avg_response_time,
            "total_casualties": total_casualties,
            "total_injuries": total_injuries,
            "active_stations": len(self.stations),
            "active_vendors": len(self.vendors),
            "incident_trend": incident_trend,
            "critical_incidents": len([i for i in self.incidents if i['severity'] == 'Critical']),
            "total_property_damage": sum(i['property_damage_inr'] for i in self.incidents)
        }
    
    def get_incidents_by_type(self):
        """Analyze incidents by type"""
        type_counts = defaultdict(int)
        for incident in self.incidents:
            type_counts[incident['incident_type']] += 1
        
        return [
            {"type": k, "count": v} 
            for k, v in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    
    def get_incidents_by_severity(self):
        """Analyze incidents by severity"""
        severity_counts = defaultdict(int)
        for incident in self.incidents:
            severity_counts[incident['severity']] += 1
        
        return [
            {"severity": k, "count": v} 
            for k, v in severity_counts.items()
        ]
    
    def get_incidents_by_state(self):
        """Analyze incidents by state"""
        state_data = defaultdict(lambda: {
            'count': 0, 
            'casualties': 0, 
            'avg_response_time': []
        })
        
        for incident in self.incidents:
            state = incident['state']
            state_data[state]['count'] += 1
            state_data[state]['casualties'] += incident['casualties']
            state_data[state]['avg_response_time'].append(incident['response_time_minutes'])
        
        result = []
        for state, data in state_data.items():
            result.append({
                "state": state,
                "incidents": data['count'],
                "casualties": data['casualties'],
                "avg_response_time": round(statistics.mean(data['avg_response_time']), 2)
            })
        
        return sorted(result, key=lambda x: x['incidents'], reverse=True)
    
    def get_monthly_trends(self):
        """Get monthly incident trends"""
        monthly_data = defaultdict(lambda: {'incidents': 0, 'casualties': 0})
        
        for incident in self.incidents:
            dt = datetime.fromisoformat(incident['timestamp'])
            month_key = dt.strftime('%Y-%m')
            monthly_data[month_key]['incidents'] += 1
            monthly_data[month_key]['casualties'] += incident['casualties']
        
        result = []
        for month, data in sorted(monthly_data.items()):
            result.append({
                "month": month,
                "incidents": data['incidents'],
                "casualties": data['casualties']
            })
        
        return result[-12:]  # Last 12 months
    
    def get_response_time_analysis(self):
        """Analyze response times by severity"""
        severity_response = defaultdict(list)
        
        for incident in self.incidents:
            severity_response[incident['severity']].append(incident['response_time_minutes'])
        
        result = []
        for severity, times in severity_response.items():
            result.append({
                "severity": severity,
                "avg_time": round(statistics.mean(times), 2),
                "min_time": min(times),
                "max_time": max(times),
                "count": len(times)
            })
        
        return result
    
    def get_vendor_performance(self):
        """Analyze vendor performance"""
        vendor_stats = defaultdict(lambda: {
            'deliveries': 0,
            'on_time': 0,
            'quality_scores': [],
            'defects': 0
        })
        
        for delivery in self.deliveries:
            vendor_id = delivery['vendor_id']
            vendor_stats[vendor_id]['deliveries'] += 1
            if delivery['on_time_status']:
                vendor_stats[vendor_id]['on_time'] += 1
            vendor_stats[vendor_id]['quality_scores'].append(delivery['quality_score'])
            vendor_stats[vendor_id]['defects'] += delivery['defect_count']
        
        # Match with vendor details
        result = []
        for vendor in self.vendors:
            vid = vendor['vendor_id']
            if vid in vendor_stats:
                stats = vendor_stats[vid]
                on_time_percentage = (stats['on_time'] / stats['deliveries'] * 100) if stats['deliveries'] > 0 else 0
                avg_quality = statistics.mean(stats['quality_scores']) if stats['quality_scores'] else 0
                
                result.append({
                    "vendor_id": vid,
                    "vendor_name": vendor['vendor_name'],
                    "vendor_type": vendor['vendor_type'],
                    "total_deliveries": stats['deliveries'],
                    "on_time_percentage": round(on_time_percentage, 2),
                    "avg_quality_score": round(avg_quality, 2),
                    "total_defects": stats['defects'],
                    "contract_value": vendor['contract_value_inr']
                })
        
        return sorted(result, key=lambda x: x['on_time_percentage'], reverse=True)
    
    def get_geographic_data(self):
        """Get geographic distribution of incidents"""
        geo_data = []
        
        # Aggregate by city
        city_incidents = defaultdict(lambda: {
            'count': 0,
            'severity_high': 0,
            'severity_critical': 0
        })
        
        for incident in self.incidents:
            city = incident['city']
            city_incidents[city]['count'] += 1
            if incident['severity'] == 'High':
                city_incidents[city]['severity_high'] += 1
            elif incident['severity'] == 'Critical':
                city_incidents[city]['severity_critical'] += 1
        
        # Match with station locations
        for station in self.stations:
            city = station['city']
            geo_data.append({
                "city": city,
                "state": station['state'],
                "latitude": station['latitude'],
                "longitude": station['longitude'],
                "incident_count": city_incidents[city]['count'],
                "high_severity": city_incidents[city]['severity_high'],
                "critical_severity": city_incidents[city]['severity_critical'],
                "station_name": station['station_name']
            })
        
        return geo_data
    
    def get_top_causes(self):
        """Get top incident causes"""
        cause_counts = defaultdict(int)
        for incident in self.incidents:
            cause_counts[incident['cause']] += 1
        
        return [
            {"cause": k, "count": v} 
            for k, v in sorted(cause_counts.items(), key=lambda x: x[1], reverse=True)
        ][:10]
    
    def search_incidents(self, filters):
        """Search incidents with filters"""
        results = self.incidents.copy()
        
        if 'state' in filters and filters['state']:
            results = [i for i in results if i['state'] == filters['state']]
        
        if 'severity' in filters and filters['severity']:
            results = [i for i in results if i['severity'] == filters['severity']]
        
        if 'incident_type' in filters and filters['incident_type']:
            results = [i for i in results if i['incident_type'] == filters['incident_type']]
        
        if 'start_date' in filters and filters['start_date']:
            start_dt = datetime.fromisoformat(filters['start_date'])
            results = [i for i in results if datetime.fromisoformat(i['timestamp']) >= start_dt]
        
        if 'end_date' in filters and filters['end_date']:
            end_dt = datetime.fromisoformat(filters['end_date'])
            results = [i for i in results if datetime.fromisoformat(i['timestamp']) <= end_dt]
        
        return results

def main():
    """Test analytics engine"""
    analytics = FireDeptAnalytics()
    
    print("=== DASHBOARD KPIs ===")
    kpis = analytics.get_dashboard_kpis()
    for key, value in kpis.items():
        print(f"{key}: {value}")
    
    print("\n=== INCIDENTS BY TYPE ===")
    by_type = analytics.get_incidents_by_type()
    for item in by_type[:5]:
        print(f"{item['type']}: {item['count']}")
    
    print("\n=== TOP STATES ===")
    by_state = analytics.get_incidents_by_state()
    for item in by_state[:5]:
        print(f"{item['state']}: {item['incidents']} incidents")
    
    print("\n=== VENDOR PERFORMANCE (Top 5) ===")
    vendors = analytics.get_vendor_performance()
    for vendor in vendors[:5]:
        print(f"{vendor['vendor_name']}: {vendor['on_time_percentage']}% on-time")
    
    print("\n✅ Analytics engine working correctly!")

if __name__ == "__main__":
    main()
