import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
from typing import Dict, Any, List

from .base_model import BaseModel

class NetworkClassifier(BaseModel):
    def __init__(self, model_path: str = None):
        super().__init__(model_path)
        if not self.model:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=None,
                min_samples_split=2,
                random_state=42
            )
        self.classes_ = None
            
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train the network traffic classifier"""
        self.model.fit(X, y)
        self.classes_ = self.model.classes_
        self.last_training_time = datetime.now()
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict traffic class"""
        return self.model.predict(X)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Get prediction probabilities for each class"""
        return self.model.predict_proba(X)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        return {
            f"feature_{i}": importance 
            for i, importance in enumerate(self.model.feature_importances_)
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = super().get_model_info()
        info.update({
            "n_classes": len(self.classes_) if self.classes_ is not None else 0,
            "n_features": self.model.n_features_in_ if hasattr(self.model, 'n_features_in_') else 0,
            "classes": self.classes_.tolist() if self.classes_ is not None else []
        })
        return info
