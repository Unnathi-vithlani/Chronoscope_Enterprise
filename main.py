#!/usr/bin/env python3
"""
CHRONOSCOPE Enterprise - Entry Point
Real-Time Criminal Behavior Observatory
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🎯 C H R O N O S C O P E  E N T E R P R I S E 🎯    ║
    ║                                                              ║
    ║      Real-Time Criminal Behavior Observatory                 ║
    ║      Criminological Threat Intelligence Platform             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

    Starting services...
    - API:  http://0.0.0.0:8000
    - Docs: http://0.0.0.0:8000/docs
    - WS:   ws://0.0.0.0:8000/ws/live

    """)

async def start():
    import uvicorn
    from api.main import app
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    banner()
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("\n🛑 CHRONOSCOPE stopped")
