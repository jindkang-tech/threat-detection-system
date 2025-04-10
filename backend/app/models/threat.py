from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

from .base import Base

class Threat(Base):
    __tablename__ = "threats"
    
    id = Column(Integer, primary_key=True, index=True)
    threat_type = Column(String, index=True)
    severity = Column(Float)
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSON)
    status = Column(String, index=True)  # detected, analyzing, resolved, false_positive
    confidence_score = Column(Float)
    
    # Relationships
    alerts = relationship("Alert", back_populates="threat")
    responses = relationship("Response", back_populates="threat")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "confidence_score": self.confidence_score,
            "raw_data": self.raw_data
        }
