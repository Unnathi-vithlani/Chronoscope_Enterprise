"""Apache Kafka Client - Enterprise Feature (Disabled on free tier)"""

from typing import Dict, List, Optional


class KafkaThreatStream:
    """Stub - install aiokafka for full distributed streaming"""

    def __init__(self, bootstrap_servers: str, client_id: str = "chronoscope"):
        pass

    async def start_producer(self): pass
    async def start_consumer(self, topic: str, group_id: str, handler): pass
    async def send_threat(self, topic: str, threat: Dict, key: Optional[str] = None): pass
    async def send_batch(self, topic: str, threats: List[Dict]): pass
    async def stop(self): pass
