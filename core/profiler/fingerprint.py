"""
Criminal Behavioral Fingerprinting

Key insight: Infrastructure rotates. Behavior persists.
A SHA-256 behavioral signature links campaigns across IP changes.
"""

from typing import Dict
from datetime import datetime
import hashlib
import json


class CriminalBehavioralFingerprint:
    """
    Generates unique behavioral signatures for threat actors.
    Unlike IOC-based tracking (IP addresses, domains),
    behavioral fingerprints persist across infrastructure rotation.
    """

    def generate(self, temporal: Dict, chronotope: Dict, threat: Dict) -> Dict:
        # Build behavioral signature from stable behavioral attributes
        sig_data = {
            'pattern': temporal.get('pattern'),
            'timezone': chronotope.get('timezone'),
            'type': chronotope.get('criminal_type'),
            'country': threat.get('country', 'Unknown'),
            'operational_hours': chronotope.get('operational_hours')
        }

        # Generate deterministic fingerprint ID
        sig_string = json.dumps(sig_data, sort_keys=True)
        fingerprint_id = hashlib.sha256(sig_string.encode()).hexdigest()[:16]

        return {
            "fingerprint_id": fingerprint_id,
            "criminal_profile": {
                "type": chronotope.get("criminal_type"),
                "timezone": chronotope.get("timezone"),
                "work_pattern": temporal.get("pattern"),
                "risk_level": chronotope.get("risk_level"),
                "sophistication": chronotope.get("sophistication"),
                "operational_hours": chronotope.get("operational_hours"),
                "geographic_origin": threat.get('country', 'Unknown')
            },
            "behavioral_signature": sig_data,
            "first_seen": datetime.utcnow().isoformat(),
            "threat_data": {
                "ip": threat.get('ip'),
                "confidence": threat.get('confidence'),
                "reports": threat.get('reports')
            }
        }
