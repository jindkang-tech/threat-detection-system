from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any
from datetime import datetime

from ...ml.pipeline import ThreatDetectionPipeline
from ...db.session import get_db, get_async_mongo_db

router = APIRouter()
pipeline = ThreatDetectionPipeline()

@router.post("/ingest/network")
async def ingest_network_data(data: Dict[str, Any]):
    """Ingest network traffic data for analysis"""
    try:
        result = await pipeline.process_network_data(data)
        return {
            "status": "success",
            "message": "Network data processed successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing network data: {str(e)}"
        )

@router.post("/ingest/logs")
async def ingest_logs(logs: List[str]):
    """Ingest log data for analysis"""
    try:
        result = await pipeline.process_log_data(logs)
        return {
            "status": "success",
            "message": "Log data processed successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing log data: {str(e)}"
        )

@router.post("/ingest/batch")
async def ingest_batch_data(data: Dict[str, Any]):
    """Ingest batch data for analysis"""
    try:
        results = []
        if "network_data" in data:
            for item in data["network_data"]:
                result = await pipeline.process_network_data(item)
                results.append(result)
                
        if "logs" in data:
            result = await pipeline.process_log_data(data["logs"])
            results.append(result)
            
        return {
            "status": "success",
            "message": "Batch data processed successfully",
            "results": results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing batch data: {str(e)}"
        )
