from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any

from .base import Base

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey("threats.id"))
    alert_type = Column(String, index=True)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_metadata = Column(JSON)
    status = Column(String, index=True)  # new, acknowledged, resolved
    
    # Relationships
    threat = relationship("Threat", back_populates="alerts")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "threat_id": self.threat_id,
            "alert_type": self.alert_type,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.alert_metadata,
            "status": self.status
        }
