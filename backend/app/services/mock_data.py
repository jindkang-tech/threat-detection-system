import random
from datetime import datetime, timedelta
import uuid

def generate_mock_threats(num_threats=10):
    threat_types = [
        "SQL Injection", "XSS Attack", "Brute Force", "DDoS", 
        "Malware Detection", "Suspicious File Access", "Unauthorized Login",
        "Data Exfiltration", "Command Injection", "Zero-day Exploit"
    ]
    
    sources = [
        "192.168.1.100", "10.0.0.15", "172.16.0.25", "192.168.0.50",
        "external_ip_1", "external_ip_2", "internal_network", "vpn_connection"
    ]
    
    threats = []
    for _ in range(num_threats):
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        threat = {
            "id": str(uuid.uuid4()),
            "type": random.choice(threat_types),
            "severity": random.randint(1, 10),
            "source": random.choice(sources),
            "target": f"asset_{random.randint(1, 100)}",
            "timestamp": timestamp.isoformat(),
            "status": random.choice(["active", "mitigated", "investigating"]),
            "confidence": random.uniform(0.5, 1.0),
            "details": {
                "attack_vector": random.choice(["network", "application", "endpoint", "cloud"]),
                "indicators": [str(uuid.uuid4()) for _ in range(random.randint(1, 3))]
            }
        }
        threats.append(threat)
    
    return sorted(threats, key=lambda x: x["timestamp"], reverse=True)

def generate_mock_alerts():
    total_alerts = random.randint(100, 500)
    resolved = random.randint(50, total_alerts - 30)
    acknowledged = random.randint(10, total_alerts - resolved - 10)
    new = total_alerts - resolved - acknowledged
    
    return {
        "total": total_alerts,
        "by_status": {
            "new": new,
            "acknowledged": acknowledged,
            "resolved": resolved
        },
        "by_severity": {
            "high": random.randint(10, 50),
            "medium": random.randint(20, 100),
            "low": random.randint(30, 150)
        },
        "response_metrics": {
            "mean_time_to_detect": random.uniform(0.5, 5.0),  # hours
            "mean_time_to_respond": random.uniform(1.0, 24.0),  # hours
            "false_positive_rate": random.uniform(0.05, 0.15)
        }
    }

def generate_mock_models():
    model_types = [
        "Anomaly Detection", "Network Traffic Analysis", 
        "User Behavior Analytics", "Malware Detection"
    ]
    
    models = []
    for i in range(random.randint(3, 6)):
        accuracy = random.uniform(0.85, 0.98)
        training_date = datetime.now() - timedelta(days=random.randint(1, 60))
        
        model = {
            "id": str(uuid.uuid4()),
            "name": f"model_{i+1}",
            "type": random.choice(model_types),
            "version": f"1.{random.randint(0, 5)}",
            "accuracy": accuracy,
            "f1_score": accuracy - random.uniform(0.02, 0.05),
            "last_trained": training_date.isoformat(),
            "status": random.choice(["active", "training", "evaluating"]),
            "metrics": {
                "precision": accuracy - random.uniform(0.01, 0.03),
                "recall": accuracy - random.uniform(0.01, 0.03),
                "false_positive_rate": random.uniform(0.01, 0.05)
            }
        }
        models.append(model)
    
    return models
