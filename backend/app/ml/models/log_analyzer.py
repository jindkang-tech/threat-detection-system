import numpy as np
from transformers import pipeline
from datetime import datetime
from typing import Dict, Any, List

from .base_model import BaseModel

class LogAnalyzer(BaseModel):
    def __init__(self, model_path: str = None):
        super().__init__(model_path)
        # Initialize BERT-based classifier for log analysis
        self.model = pipeline(
            "text-classification",
            model="bert-base-uncased",
            top_k=None
        )
        self.label_map = {
            "NORMAL": 0,
            "WARNING": 1,
            "CRITICAL": 2
        }
            
    def train(self, X: np.ndarray, y: np.ndarray = None) -> None:
        """Training not implemented for pre-trained model"""
        pass
        
    def predict(self, X: List[str]) -> List[str]:
        """Predict log severity"""
        results = self.model(X)
        predictions = []
        for result in results:
            # Get the label with highest score
            pred = max(result, key=lambda x: x['score'])
            predictions.append(pred['label'])
        return predictions
    
    def predict_proba(self, X: List[str]) -> List[Dict[str, float]]:
        """Get prediction probabilities for each severity level"""
        results = self.model(X)
        probabilities = []
        for result in results:
            prob_dict = {pred['label']: pred['score'] for pred in result}
            probabilities.append(prob_dict)
        return probabilities
    
    def analyze_log_pattern(self, logs: List[str]) -> Dict[str, Any]:
        """Analyze patterns in a sequence of logs"""
        predictions = self.predict(logs)
        severity_counts = {
            severity: predictions.count(severity)
            for severity in self.label_map.keys()
        }
        return {
            "severity_distribution": severity_counts,
            "critical_count": severity_counts.get("CRITICAL", 0),
            "warning_count": severity_counts.get("WARNING", 0),
            "normal_count": severity_counts.get("NORMAL", 0)
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = super().get_model_info()
        info.update({
            "model_type": "BERT-based Log Analyzer",
            "supported_severities": list(self.label_map.keys())
        })
        return info
