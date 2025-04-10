import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
from typing import Dict, Any

from .base_model import BaseModel

class AnomalyDetector(BaseModel):
    def __init__(self, model_path: str = None, contamination: float = 0.1):
        super().__init__(model_path)
        self.contamination = contamination
        if not self.model:
            self.model = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
            
    def train(self, X: np.ndarray, y: np.ndarray = None) -> None:
        """Train the anomaly detection model"""
        self.model.fit(X)
        self.last_training_time = datetime.now()
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict anomalies. Returns -1 for anomalies and 1 for normal samples"""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get anomaly scores"""
        return -self.model.score_samples(X)
    
    def get_threshold(self) -> float:
        """Get the anomaly threshold"""
        return -self.model.offset_
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = super().get_model_info()
        info.update({
            "contamination": self.contamination,
            "n_estimators": self.model.n_estimators
        })
        return info
