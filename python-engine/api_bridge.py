#!/usr/bin/env python3
"""
API Bridge - Python script called by Node.js backend
Returns JSON data for various analytics endpoints
"""
import sys
import json
from analytics import FireDeptAnalytics
from report_generator import ReportGenerator

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        sys.exit(1)
    
    command = sys.argv[1]
    analytics = FireDeptAnalytics()
    
    try:
        if command == "get_kpis":
            result = analytics.get_dashboard_kpis()
        
        elif command == "get_incidents_by_type":
            result = analytics.get_incidents_by_type()
        
        elif command == "get_incidents_by_severity":
            result = analytics.get_incidents_by_severity()
        
        elif command == "get_state_analysis":
            result = analytics.get_incidents_by_state()
        
        elif command == "get_monthly_trends":
            result = analytics.get_monthly_trends()
        
        elif command == "get_response_time":
            result = analytics.get_response_time_analysis()
        
        elif command == "get_vendor_performance":
            result = analytics.get_vendor_performance()
        
        elif command == "get_geographic_data":
            result = analytics.get_geographic_data()
        
        elif command == "get_top_causes":
            result = analytics.get_top_causes()
        
        elif command == "search_incidents":
            if len(sys.argv) < 3:
                result = {"error": "No filters provided"}
            else:
                filters = json.loads(sys.argv[2])
                result = analytics.search_incidents(filters)
        
        elif command == "generate_pdf_report":
            generator = ReportGenerator()
            file_path = generator.generate_executive_report_pdf()
            result = {"success": True, "file_path": file_path}
        
        elif command == "generate_excel_report":
            generator = ReportGenerator()
            file_path = generator.generate_excel_report()
            result = {"success": True, "file_path": file_path}
        
        else:
            result = {"error": f"Unknown command: {command}"}
        
        print(json.dumps(result))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
