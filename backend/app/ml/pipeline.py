from typing import Dict, Any, List
import asyncio
from datetime import datetime
import logging

from .preprocessing import DataPreprocessor
from .feature_extraction import FeatureExtractor
from .models.anomaly_detector import AnomalyDetector
from .models.network_classifier import NetworkClassifier
from .models.log_analyzer import LogAnalyzer
from ..models.threat import Threat
from ..models.alert import Alert
from ..db.session import get_db, get_async_mongo_db

logger = logging.getLogger(__name__)

class ThreatDetectionPipeline:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.feature_extractor = FeatureExtractor()
        self.anomaly_detector = AnomalyDetector()
        self.network_classifier = NetworkClassifier()
        self.log_analyzer = LogAnalyzer()
        
    async def process_network_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process network traffic data"""
        try:
            # Preprocess data
            processed_data = self.preprocessor.preprocess_network_data(data)
            
            # Extract features
            features = self.feature_extractor.extract_network_features(data)
            
            # Run anomaly detection
            anomaly_score = self.anomaly_detector.predict_proba(features.reshape(1, -1))[0]
            
            # Classify traffic
            traffic_type = self.network_classifier.predict(features.reshape(1, -1))[0]
            confidence = max(self.network_classifier.predict_proba(features.reshape(1, -1))[0])
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "anomaly_score": float(anomaly_score),
                "traffic_type": traffic_type,
                "confidence": float(confidence),
                "raw_data": data
            }
            
            # Generate threat if anomaly detected
            if anomaly_score > 0.8:  # Threshold for anomaly
                await self._create_threat(result)
                
            return result
            
        except Exception as e:
            logger.error(f"Error processing network data: {str(e)}")
            raise
            
    async def process_log_data(self, logs: List[str]) -> Dict[str, Any]:
        """Process log data"""
        try:
            # Analyze logs
            severity_analysis = self.log_analyzer.analyze_log_pattern(logs)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "severity_analysis": severity_analysis,
                "raw_logs": logs
            }
            
            # Generate threat if critical logs detected
            if severity_analysis["critical_count"] > 0:
                await self._create_threat(result, threat_type="log_based")
                
            return result
            
        except Exception as e:
            logger.error(f"Error processing log data: {str(e)}")
            raise
            
    async def _create_threat(self, data: Dict[str, Any], threat_type: str = "network_based") -> None:
        """Create a threat entry and associated alert"""
        mongo_db = get_async_mongo_db()
        
        # Store raw data in MongoDB
        raw_data_id = await mongo_db.raw_data.insert_one(data)
        
        # Create threat in PostgreSQL
        threat = Threat(
            threat_type=threat_type,
            severity=float(data.get("anomaly_score", 0.9)),
            source_ip=data.get("raw_data", {}).get("source_ip"),
            destination_ip=data.get("raw_data", {}).get("destination_ip"),
            raw_data={"mongo_id": str(raw_data_id.inserted_id)},
            status="detected",
            confidence_score=float(data.get("confidence", 0.8))
        )
        
        # Create alert
        alert = Alert(
            threat=threat,
            alert_type=f"{threat_type}_threat",
            message=f"Potential {threat_type} threat detected",
            status="new",
            metadata=data
        )
        
        db = next(get_db())
        try:
            db.add(threat)
            db.add(alert)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
        finally:
            db.close()
