from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any

from ...services.mock_data import generate_mock_threats

router = APIRouter()

@router.get("/threats", response_model=List[Dict[str, Any]])
async def get_threats(limit: int = Query(10, ge=1, le=100)):
    """Get list of detected threats"""
    return generate_mock_threats(limit)

@router.get("/threats/{threat_id}")
async def get_threat(threat_id: str):
    """Get specific threat details"""
    threats = generate_mock_threats(100)
    for threat in threats:
        if threat['id'] == threat_id:
            return threat
    raise HTTPException(status_code=404, detail="Threat not found")

@router.post("/threats/analyze")
async def analyze_threat(data: Dict):
    """Analyze potential threat"""
    return {"status": "analyzing", "data": data}

@router.post("/threats/{threat_id}/respond")
async def respond_to_threat(threat_id: str, action: Dict):
    """Respond to a specific threat"""
    return {"status": "response_initiated", "threat_id": threat_id}
