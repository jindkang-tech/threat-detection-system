from abc import ABC, abstractmethod
from typing import Any, Dict, List
import numpy as np
import joblib
from datetime import datetime

class BaseModel(ABC):
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_path = model_path
        self.last_training_time = None
        
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray = None) -> None:
        """Train the model"""
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        pass
    
    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities"""
        pass
    
    def save_model(self, path: str = None) -> None:
        """Save model to disk"""
        save_path = path or self.model_path
        if save_path and self.model:
            joblib.dump(self.model, save_path)
            
    def load_model(self, path: str = None) -> None:
        """Load model from disk"""
        load_path = path or self.model_path
        if load_path:
            self.model = joblib.load(load_path)
            
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_type": self.__class__.__name__,
            "last_training_time": self.last_training_time,
            "model_path": self.model_path
        }
