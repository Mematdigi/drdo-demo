#!/usr/bin/env python3
"""
Generate sample fire department data for demo
"""
import json
import random
from datetime import datetime, timedelta
import uuid

# Indian states and major cities
STATES_CITIES = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Karol Bagh"],
    "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"]
}

INCIDENT_TYPES = [
    "Building Fire", "Vehicle Fire", "Forest Fire", "Industrial Fire",
    "Electrical Fire", "Kitchen Fire", "Chemical Fire", "Gas Leak"
]

SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]

CAUSES = [
    "Electrical Short Circuit", "Gas Leak", "Kitchen Negligence", 
    "Smoking", "Arson", "Industrial Accident", "Natural Causes",
    "Equipment Malfunction", "Unknown"
]

# Vendor data
VENDOR_TYPES = ["Equipment Supplier", "Maintenance Service", "Training Provider", "Safety Gear Supplier"]
VENDOR_NAMES = [
    "FireSafe India Pvt Ltd", "SafeGuard Equipment Co", "Blaze Control Systems",
    "Emergency Response Solutions", "ProTech Safety Gear", "National Fire Services",
    "Advanced Safety Equipment", "FireShield Technologies", "RapidResponse Suppliers",
    "SecureLife Fire Systems", "Guardian Safety Solutions", "Alert Fire Protection"
]

def generate_incidents(count=500):
    """Generate sample incident data"""
    incidents = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(count):
        state = random.choice(list(STATES_CITIES.keys()))
        city = random.choice(STATES_CITIES[state])
        
        # Generate timestamp
        days_ago = random.randint(0, 365)
        incident_time = start_date + timedelta(days=days_ago, 
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))
        
        severity = random.choice(SEVERITY_LEVELS)
        incident_type = random.choice(INCIDENT_TYPES)
        
        # Response time based on severity (lower for critical)
        if severity == "Critical":
            response_time = random.randint(5, 15)
            resolution_time = random.randint(120, 300)
        elif severity == "High":
            response_time = random.randint(10, 25)
            resolution_time = random.randint(60, 180)
        elif severity == "Medium":
            response_time = random.randint(15, 35)
            resolution_time = random.randint(30, 120)
        else:
            response_time = random.randint(20, 45)
            resolution_time = random.randint(15, 60)
        
        # Casualties based on severity
        if severity == "Critical":
            casualties = random.randint(0, 5)
            injuries = random.randint(5, 20)
        elif severity == "High":
            casualties = random.randint(0, 2)
            injuries = random.randint(2, 10)
        else:
            casualties = 0
            injuries = random.randint(0, 3)
        
        incident = {
            "incident_id": str(uuid.uuid4()),
            "timestamp": incident_time.isoformat(),
            "state": state,
            "district": city + " District",
            "city": city,
            "location": f"{random.randint(1, 500)}, {random.choice(['MG Road', 'Main Street', 'Park Avenue', 'Station Road', 'Market Road'])}",
            "latitude": round(random.uniform(8.0, 35.0), 6),
            "longitude": round(random.uniform(68.0, 97.0), 6),
            "incident_type": incident_type,
            "severity": severity,
            "response_time_minutes": response_time,
            "resolution_time_minutes": resolution_time,
            "casualties": casualties,
            "injuries": injuries,
            "property_damage_inr": random.randint(50000, 10000000) if severity in ["High", "Critical"] else random.randint(10000, 500000),
            "station_id": f"FS-{state[:3].upper()}-{random.randint(1, 50):03d}",
            "vehicles_deployed": random.randint(1, 6),
            "personnel_count": random.randint(4, 25),
            "equipment_used": random.sample(["Fire Truck", "Water Tanker", "Ladder", "Breathing Apparatus", "Fire Extinguisher", "Rescue Equipment"], k=random.randint(2, 4)),
            "cause": random.choice(CAUSES),
            "remarks": f"Incident resolved successfully. {random.choice(['No casualties reported', 'Minor injuries treated on site', 'Area secured', 'Investigation ongoing'])}"
        }
        incidents.append(incident)
    
    return incidents

def generate_vendors(count=50):
    """Generate sample vendor data"""
    vendors = []
    
    for i in range(count):
        vendor_id = str(uuid.uuid4())
        vendor_name = random.choice(VENDOR_NAMES) + f" - {chr(65 + i % 26)}"
        vendor_type = random.choice(VENDOR_TYPES)
        
        # Generate contract dates
        contract_start = datetime.now() - timedelta(days=random.randint(180, 1095))
        contract_end = contract_start + timedelta(days=random.randint(365, 1825))
        
        vendor = {
            "vendor_id": vendor_id,
            "vendor_name": vendor_name,
            "vendor_type": vendor_type,
            "registration_no": f"REG-{random.randint(10000, 99999)}",
            "contact_person": random.choice(["Rajesh Kumar", "Amit Sharma", "Priya Patel", "Suresh Reddy", "Anil Gupta"]),
            "email": f"{vendor_name.lower().replace(' ', '.')}@company.com",
            "phone": f"+91-{random.randint(7000000000, 9999999999)}",
            "address": f"{random.randint(1, 200)}, Sector {random.randint(1, 50)}, {random.choice(list(STATES_CITIES.keys()))}",
            "contract_id": f"CNT-{random.randint(1000, 9999)}",
            "contract_start_date": contract_start.date().isoformat(),
            "contract_end_date": contract_end.date().isoformat(),
            "contract_value_inr": random.randint(1000000, 50000000),
            "performance_score": round(random.uniform(3.0, 5.0), 2),
            "total_deliveries": random.randint(5, 50)
        }
        vendors.append(vendor)
    
    return vendors

def generate_vendor_deliveries(vendors, count=200):
    """Generate vendor delivery records"""
    deliveries = []
    
    for i in range(count):
        vendor = random.choice(vendors)
        delivery_date = datetime.now() - timedelta(days=random.randint(0, 365))
        
        # On-time delivery probability based on vendor score
        on_time = random.random() < (vendor["performance_score"] / 5.0)
        
        delivery = {
            "delivery_id": str(uuid.uuid4()),
            "vendor_id": vendor["vendor_id"],
            "vendor_name": vendor["vendor_name"],
            "delivery_date": delivery_date.date().isoformat(),
            "items_delivered": random.choice(["Fire Extinguishers", "Safety Helmets", "Protective Gear", 
                                             "Breathing Apparatus", "Fire Hoses", "Communication Equipment"]),
            "quantity": random.randint(10, 500),
            "on_time_status": on_time,
            "quality_score": round(random.uniform(3.5, 5.0), 2),
            "defect_count": random.randint(0, 5) if not on_time else random.randint(0, 2),
            "issue_description": "" if on_time and random.random() > 0.2 else random.choice([
                "Minor packaging damage", "Delayed delivery", "Quality issues", 
                "Incomplete order", "Documentation missing", "No issues"
            ])
        }
        deliveries.append(delivery)
    
    return deliveries

def generate_fire_stations():
    """Generate fire station data"""
    stations = []
    station_id = 1
    
    for state, cities in STATES_CITIES.items():
        for city in cities:
            num_stations = random.randint(2, 5)
            for i in range(num_stations):
                station = {
                    "station_id": f"FS-{state[:3].upper()}-{station_id:03d}",
                    "station_name": f"{city} Fire Station {i+1}",
                    "state": state,
                    "city": city,
                    "address": f"Station Road {i+1}, {city}",
                    "latitude": round(random.uniform(8.0, 35.0), 6),
                    "longitude": round(random.uniform(68.0, 97.0), 6),
                    "personnel_count": random.randint(15, 50),
                    "vehicles": random.randint(3, 10),
                    "established_year": random.randint(1990, 2020),
                    "coverage_area_sqkm": random.randint(10, 100)
                }
                stations.append(station)
                station_id += 1
    
    return stations

def main():
    """Generate all sample data"""
    print("Generating sample data for Fire Department Analytics Demo...")
    
    # Generate data
    incidents = generate_incidents(500)
    vendors = generate_vendors(50)
    deliveries = generate_vendor_deliveries(vendors, 200)
    stations = generate_fire_stations()
    
    # Save to JSON files
    data_dir = "/home/claude/fire-dept-demo/data"
    
    with open(f"{data_dir}/incidents.json", "w") as f:
        json.dump(incidents, f, indent=2)
    print(f"✓ Generated {len(incidents)} incidents")
    
    with open(f"{data_dir}/vendors.json", "w") as f:
        json.dump(vendors, f, indent=2)
    print(f"✓ Generated {len(vendors)} vendors")
    
    with open(f"{data_dir}/vendor_deliveries.json", "w") as f:
        json.dump(deliveries, f, indent=2)
    print(f"✓ Generated {len(deliveries)} vendor deliveries")
    
    with open(f"{data_dir}/fire_stations.json", "w") as f:
        json.dump(stations, f, indent=2)
    print(f"✓ Generated {len(stations)} fire stations")
    
    print("\n✅ Sample data generation complete!")
    print(f"Data saved to: {data_dir}/")

if __name__ == "__main__":
    main()
