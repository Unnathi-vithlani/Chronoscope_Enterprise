"""PostgreSQL Cache - Enterprise Feature (Disabled on free tier)"""

from typing import Optional, Dict, Any


class EnterpriseThreatCache:
    """Stub - requires asyncpg and redis for enterprise deployment"""

    def __init__(self, database_url: str, redis_url: str):
        raise NotImplementedError("Enterprise feature: pip install asyncpg redis")

    async def connect(self): pass
    async def store_threat(self, threat: Dict, ttl: int = 3600) -> bool: return False
    async def get_threat(self, ip: str) -> Optional[Dict]: return None
    async def get_stats(self) -> Dict[str, Any]: return {"error": "Not configured"}
    async def close(self): pass
