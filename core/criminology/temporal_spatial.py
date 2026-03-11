"""
Temporal-Spatial Criminological Analysis
Based on Routine Activity Theory (Cohen & Felson, 1979)
"""

from typing import Dict


class AdversarialChronotope:
    """
    Analyzes the temporal-spatial relationship in attack patterns
    to infer threat actor behavioral profiles.

    Theory: Professional criminal actors operate on professional schedules.
    Their operational hours reveal organizational sophistication,
    geographic origin, and likely criminal type.
    """

    def analyze(self, temporal: Dict, spatial: Dict = None) -> Dict:
        avg_hour = temporal.get('avg_hour', 12)
        pattern = temporal.get('pattern', 'unknown')
        reports = temporal.get('reports_count', 0)

        # Timezone and initial profile inference from operational hours
        if 6 <= avg_hour <= 14:
            timezone = "eastern_europe"
            profile = "PROFESSIONAL_ORGANIZED_CRIME"
        elif 14 <= avg_hour <= 22:
            timezone = "western_europe"
            profile = "MODERATE_PROFESSIONAL"
        else:
            timezone = "americas"
            profile = "VARIED_ACTOR"

        # Refine profile based on behavioral pattern
        if pattern == 'professional':
            profile = "PROFESSIONAL_ORGANIZED_CRIME"
            risk_level = "high"
        elif pattern == 'irregular':
            profile = "OPPORTUNISTIC_SCRIPT_KIDDIE"
            risk_level = "medium"
        else:
            risk_level = "low"

        # Sophistication based on report volume
        sophistication = (
            "expert" if reports > 100
            else "moderate" if reports > 50
            else "novice"
        )

        return {
            "criminal_type": profile,
            "timezone": timezone,
            "work_pattern": pattern,
            "risk_level": risk_level,
            "sophistication": sophistication,
            "operational_hours": f"{int(avg_hour-2):02d}:00-{int(avg_hour+2):02d}:00"
        }
