"""AbuseIPDB Data Ingestor"""

import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AbuseIPDBIngestor:
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.base_url = "https://api.abuseipdb.com/api/v2"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"Key": self.api_key, "Accept": "application/json"}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_blacklist(self, limit: int = 100) -> List[Dict]:
        if not self.api_key:
            logger.error("No API key provided")
            return []

        url = f"{self.base_url}/blacklist"
        params = {"confidenceMinimum": 75, "limit": limit}

        try:
            async with self.session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    threats = data.get('data', [])
                    logger.info(f"Retrieved {len(threats)} threats from AbuseIPDB")
                    return threats
                else:
                    text = await response.text()
                    logger.error(f"HTTP {response.status}: {text[:200]}")
                    return []
        except Exception as e:
            logger.error(f"Blacklist fetch error: {e}")
            return []

    async def check_ip(self, ip: str) -> Dict:
        url = f"{self.base_url}/check"
        params = {"ipAddress": ip, "maxAgeInDays": 90, "verbose": True}

        try:
            async with self.session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._extract_temporal(data.get('data', {}))
                return {}
        except Exception as e:
            logger.error(f"IP check failed for {ip}: {e}")
            return {}

    def _extract_temporal(self, data: Dict) -> Dict:
        """Extract temporal patterns from IP report history"""
        reports = data.get('reports', [])
        if not reports:
            return {}

        hours = []
        for r in reports:
            try:
                ts = r.get('reportedAt', '')
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                hours.append(dt.hour)
            except Exception:
                pass

        if not hours:
            return {}

        avg = sum(hours) / len(hours)
        spread = max(hours) - min(hours)

        return {
            'avg_hour': round(avg, 1),
            'pattern': 'professional' if spread < 8 else 'irregular',
            'timezone': 'eastern_europe' if 6 <= avg <= 14 else 'unknown',
            'reports_count': len(hours)
        }
