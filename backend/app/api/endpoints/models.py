from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from datetime import datetime

from ...services.mock_data import generate_mock_models

router = APIRouter()

@router.get("/models", response_model=List[Dict[str, Any]])
async def list_models():
    """List all available models and their information"""
    return generate_mock_models()

@router.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """Get specific model information"""
    models = generate_mock_models()
    for model in models:
        if model['name'] == model_name:
            return model
    raise HTTPException(status_code=404, detail="Model not found")
    return models[model_name].get_model_info()

@router.post("/models/{model_name}/train")
async def train_model(model_name: str, training_data: Dict[str, Any]):
    """Train a specific model"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Extract features and labels from training data
        X = training_data.get("features")
        y = training_data.get("labels")
        
        if not X:
            raise HTTPException(status_code=400, detail="No features provided")
            
        # Train the model
        models[model_name].train(X, y)
        
        return {
            "status": "success",
            "message": f"Model {model_name} trained successfully",
            "model_info": models[model_name].get_model_info()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error training model: {str(e)}"
        )

@router.post("/models/{model_name}/predict")
async def predict(model_name: str, data: Dict[str, Any]):
    """Make predictions using a specific model"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        # Get predictions
        predictions = models[model_name].predict(data["features"])
        probabilities = models[model_name].predict_proba(data["features"])
        
        return {
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error making predictions: {str(e)}"
        )

@router.post("/models/{model_name}/save")
async def save_model(model_name: str, path: str):
    """Save model to disk"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        models[model_name].save_model(path)
        return {"status": "success", "message": f"Model {model_name} saved successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving model: {str(e)}"
        )

@router.post("/models/{model_name}/load")
async def load_model(model_name: str, path: str):
    """Load model from disk"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        models[model_name].load_model(path)
        return {"status": "success", "message": f"Model {model_name} loaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading model: {str(e)}"
        )
