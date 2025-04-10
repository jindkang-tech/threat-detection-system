from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

class FeatureExtractor:
    def __init__(self):
        self.text_vectorizer = TfidfVectorizer(max_features=100)
        
    def extract_network_features(self, network_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from network traffic data"""
        features = []
        
        # Basic network features
        features.extend([
            network_data.get('bytes_sent', 0),
            network_data.get('bytes_received', 0),
            network_data.get('duration', 0),
            network_data.get('protocol_type', 0)
        ])
        
        # Time-based features
        timestamp = network_data.get('timestamp')
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
            features.extend([
                dt.hour,
                dt.minute,
                dt.weekday()
            ])
            
        return np.array(features)
    
    def extract_log_features(self, log_data: Dict[str, Any]) -> np.ndarray:
        """Extract features from log data"""
        features = []
        
        # Log severity
        severity_map = {'INFO': 0, 'WARNING': 1, 'ERROR': 2, 'CRITICAL': 3}
        features.append(severity_map.get(log_data.get('severity', 'INFO'), 0))
        
        # Log message vectorization
        if 'message' in log_data:
            message_vector = self.text_vectorizer.fit_transform([log_data['message']]).toarray()
            features.extend(message_vector.flatten())
            
        return np.array(features)
    
    def combine_features(self, features_list: List[np.ndarray]) -> np.ndarray:
        """Combine multiple feature arrays"""
        return np.concatenate(features_list)
