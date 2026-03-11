"""CHRONOSCOPE Enterprise API — Render.com Ready"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime
from typing import Dict
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import SETTINGS
from core.database.local_cache import ThreatCache
from core.ingestors.abuseipdb import AbuseIPDBIngestor
from core.criminology.temporal_spatial import AdversarialChronotope
from core.profiler.fingerprint import CriminalBehavioralFingerprint

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

cache = None
clients = []
profiles_db = {}

# Demo data — pre-profiled threat actors for immediate demonstration
DEMO_THREATS = [
    {
        "ip": "185.220.101.42",
        "confidence": 95,
        "reports": 127,
        "country": "RU",
        "temporal": {"avg_hour": 10.5, "pattern": "professional", "reports_count": 127}
    },
    {
        "ip": "192.42.116.191",
        "confidence": 88,
        "reports": 89,
        "country": "NL",
        "temporal": {"avg_hour": 14.2, "pattern": "professional", "reports_count": 89}
    },
    {
        "ip": "103.75.201.4",
        "confidence": 82,
        "reports": 56,
        "country": "CN",
        "temporal": {"avg_hour": 3.1, "pattern": "irregular", "reports_count": 56}
    },
    {
        "ip": "45.142.212.100",
        "confidence": 91,
        "reports": 143,
        "country": "BG",
        "temporal": {"avg_hour": 9.8, "pattern": "professional", "reports_count": 143}
    },
    {
        "ip": "198.98.51.189",
        "confidence": 76,
        "reports": 34,
        "country": "US",
        "temporal": {"avg_hour": 18.5, "pattern": "irregular", "reports_count": 34}
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    global cache

    logger.info("=" * 50)
    logger.info("Starting CHRONOSCOPE Enterprise")
    logger.info("=" * 50)

    cache = ThreatCache()
    logger.info("SQLite cache initialized")

    asyncio.create_task(ingest_loop())

    logger.info(f"Mode: {'DEMO' if SETTINGS.DEMO_MODE else 'LIVE'}")
    logger.info("CHRONOSCOPE READY")
    logger.info("=" * 50)

    yield

    logger.info("Shutting down CHRONOSCOPE...")


app = FastAPI(
    title="CHRONOSCOPE Enterprise",
    description="Real-Time Criminal Behavior Observatory — Criminological Threat Intelligence",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def process_threat(threat_raw: Dict, source: str = "api") -> Dict:
    """Run a threat through the full criminological profiling pipeline"""
    chronotope = AdversarialChronotope()
    temporal = threat_raw.get('temporal', {})
    analysis = chronotope.analyze(temporal, {})

    profiler = CriminalBehavioralFingerprint()
    profile = profiler.generate(temporal, analysis, threat_raw)

    cache.store(threat_raw['ip'], profile)
    profiles_db[profile['fingerprint_id']] = profile

    logger.info(
        f"Profiled {threat_raw['ip']} → {profile['criminal_profile']['type']} "
        f"[{profile['criminal_profile']['risk_level']}]"
    )
    return profile


async def ingest_loop():
    await asyncio.sleep(2)

    if SETTINGS.DEMO_MODE:
        await run_demo_mode()
    else:
        await run_live_mode()


async def run_demo_mode():
    logger.info("Running in DEMO mode")

    for threat in DEMO_THREATS:
        profile = await process_threat(threat, "demo")
        await broadcast({
            "type": "new_threat",
            "data": profile,
            "timestamp": datetime.utcnow().isoformat()
        })
        await asyncio.sleep(1)

    logger.info(f"Demo loaded: {len(profiles_db)} criminal profiles active")

    # Keep-alive heartbeat
    while True:
        await asyncio.sleep(30)
        await broadcast({
            "type": "heartbeat",
            "profiles": len(profiles_db),
            "timestamp": datetime.utcnow().isoformat()
        })


async def run_live_mode():
    logger.info("Running in LIVE mode — ingesting from AbuseIPDB")

    while True:
        try:
            async with AbuseIPDBIngestor(SETTINGS.ABUSEIPDB_KEY) as ingestor:
                threats = await ingestor.get_blacklist(limit=50)

                for t in threats:
                    ip = t.get('ipAddress')
                    if cache.get(ip):
                        continue

                    temporal = await ingestor.check_ip(ip)
                    threat_obj = {
                        "ip": ip,
                        "confidence": t.get('abuseConfidencePercentage', 0),
                        "reports": t.get('totalReports', 0),
                        "country": t.get('countryCode', 'Unknown'),
                        "temporal": temporal or {"avg_hour": 12, "pattern": "unknown"}
                    }

                    profile = await process_threat(threat_obj, "abuseipdb")
                    await broadcast({
                        "type": "new_threat",
                        "data": profile,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                await asyncio.sleep(300)

        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            await asyncio.sleep(60)


async def broadcast(message: dict):
    """Broadcast to all connected WebSocket clients"""
    disconnected = []
    for conn in clients:
        try:
            await conn.send_json(message)
        except Exception:
            disconnected.append(conn)

    for conn in disconnected:
        if conn in clients:
            clients.remove(conn)


@app.get("/")
async def root():
    return {
        "service": "CHRONOSCOPE Enterprise",
        "version": "2.0.0",
        "description": "Real-Time Criminal Behavior Observatory",
        "status": "operational",
        "mode": "DEMO" if SETTINGS.DEMO_MODE else "LIVE",
        "profiles_active": len(profiles_db),
        "cache_stats": cache.stats() if cache else {},
        "endpoints": {
            "threats": "/threats/live",
            "websocket": "/ws/live",
            "docs": "/docs"
        }
    }


@app.get("/threats/live")
async def get_threats(limit: int = 50):
    threats = list(profiles_db.values())[-limit:]
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "profiles": threats,
        "total": len(profiles_db),
        "mode": "DEMO" if SETTINGS.DEMO_MODE else "LIVE"
    }


@app.get("/criminals/{fingerprint_id}")
async def get_criminal(fingerprint_id: str):
    profile = profiles_db.get(fingerprint_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Criminal profile not found")
    return {"profile": profile}


@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    logger.info(f"WebSocket client connected. Active clients: {len(clients)}")

    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "profiles_tracked": len(profiles_db),
            "mode": "DEMO" if SETTINGS.DEMO_MODE else "LIVE",
            "message": "Connected to CHRONOSCOPE Criminal Behavior Observatory"
        })

        # Send recent profiles on connect
        for profile in list(profiles_db.values())[-10:]:
            await websocket.send_json({
                "type": "new_threat",
                "data": profile,
                "timestamp": datetime.utcnow().isoformat()
            })

        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            await websocket.send_json({
                "type": "heartbeat",
                "profiles": len(profiles_db),
                "timestamp": datetime.utcnow().isoformat()
            })

    except WebSocketDisconnect:
        pass
    finally:
        if websocket in clients:
            clients.remove(websocket)
        logger.info(f"Client disconnected. Active clients: {len(clients)}")
