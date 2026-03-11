"""CHRONOSCOPE Configuration"""

import os
from dataclasses import dataclass

@dataclass
class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///chronoscope.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
    KAFKA_THREAT_TOPIC: str = os.getenv("KAFKA_THREAT_TOPIC", "threats.raw")
    KAFKA_PROFILED_TOPIC: str = os.getenv("KAFKA_PROFILED_TOPIC", "threats.profiled")
    ABUSEIPDB_KEY: str = os.getenv("ABUSEIPDB_KEY", "")
    URLHAUS_KEY: str = os.getenv("URLHAUS_KEY", "")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "True").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "")
    SPARK_MASTER: str = os.getenv("SPARK_MASTER", "local[*]")
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "2"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "50"))

SETTINGS = Settings()
