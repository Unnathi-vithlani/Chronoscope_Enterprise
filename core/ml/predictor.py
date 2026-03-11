"""ML Pipeline - Enterprise Feature (Disabled on free tier)"""

from typing import Dict, List
from datetime import datetime


class MLPredictor:
    """Stub for free tier — enables ML features when mlflow/spark installed"""

    def __init__(self): pass

    def predict_next_targets(self, current_threats: List[Dict]) -> Dict:
        return {
            "predicted_timezone": "unknown",
            "predicted_criminal_type": "unknown",
            "confidence": 0.0,
            "recommended_defenses": ["Enable full ML pipeline"],
            "generated_at": datetime.utcnow().isoformat()
        }

    def detect_anomalies(self, new_threat: Dict) -> Dict:
        return {"is_anomaly": False, "confidence": 0.5}
