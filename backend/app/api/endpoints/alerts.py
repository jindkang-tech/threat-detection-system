from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

from ...services.mock_data import generate_mock_alerts

router = APIRouter()

@router.get("/alerts", response_model=List[Dict[str, Any]])
async def get_alerts(
    status: str = Query(None, enum=["new", "acknowledged", "resolved"]),
    limit: int = 100,
    skip: int = 0
):
    """Get list of alerts with optional filtering"""
    alert_data = generate_mock_alerts()
    alerts = []
    for i in range(limit):
        alerts.append({
            "id": i + 1,
            "title": f"Alert {i + 1}",
            "description": f"Mock alert description {i + 1}",
            "severity": "high" if i % 3 == 0 else "medium" if i % 3 == 1 else "low",
            "status": status if status else random.choice(["new", "acknowledged", "resolved"]),
            "created_at": (datetime.now() - timedelta(hours=i)).isoformat(),
            "updated_at": datetime.now().isoformat()
        })
    return alerts[skip:skip+limit]

@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: int):
    """Get specific alert details"""
    if alert_id < 1 or alert_id > 100:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "id": alert_id,
        "title": f"Alert {alert_id}",
        "description": f"Detailed mock alert description {alert_id}",
        "severity": "high" if alert_id % 3 == 0 else "medium" if alert_id % 3 == 1 else "low",
        "status": random.choice(["new", "acknowledged", "resolved"]),
        "created_at": (datetime.now() - timedelta(hours=alert_id)).isoformat(),
        "updated_at": datetime.now().isoformat(),
        "details": {
            "source_ip": f"192.168.1.{alert_id % 255}",
            "destination_ip": f"10.0.0.{alert_id % 255}",
            "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
            "port": random.randint(1, 65535)
        }
    }


@router.put("/alerts/{alert_id}/status")
async def update_alert_status(
    alert_id: int,
    status: str = Query(..., enum=["acknowledged", "resolved"])
):
    """Update alert status"""
    if alert_id < 1 or alert_id > 100:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "id": alert_id,
        "status": status,
        "updated_at": datetime.now().isoformat(),
        "message": "Alert status updated successfully"
    }

@router.post("/alerts/{alert_id}/comment")
async def add_alert_comment(
    alert_id: int,
    comment: Dict[str, str]
):
    """Add comment to an alert"""
    if alert_id < 1 or alert_id > 100:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "id": alert_id,
        "comment": {
            "text": comment["text"],
            "timestamp": datetime.now().isoformat(),
            "user": "system"
        },
        "message": "Comment added successfully"
    }

@router.get("/statistics")
async def get_alert_statistics():
    """Get alert statistics"""
    return generate_mock_alerts()
