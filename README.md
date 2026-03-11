# 🎯 CHRONOSCOPE
### Real-Time Criminal Behavior Observatory for Cybersecurity Threat Intelligence

> Applying 100 years of criminological theory to live threat data.

[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://chronoscope-enterprise.onrender.com)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

---

## The Problem

Threat intelligence platforms are excellent at tracking *what* attacks happen
and *where* they come from.

They almost never ask *why* — or *who*.

Criminologists have studied offender behavior for over a century.
Routine Activity Theory. Temporal-spatial analysis. Behavioral fingerprinting.
These frameworks reliably predict criminal behavior in physical contexts.

Nobody was applying them to live cyber threat data in real time.

**Chronoscope does.**

---

## What It Does

Chronoscope ingests live threat feeds and runs each threat actor through
a criminological profiling engine that generates:

- **Behavioral type classification** — Professional organized crime vs.
  opportunistic actor vs. script kiddie, based on operational patterns
- **Temporal-spatial fingerprint** — When and from where this actor operates,
  inferred from attack timing patterns
- **Criminal behavioral signature** — A unique identifier that persists
  across IP rotation, linking campaigns by behavior not infrastructure
- **Risk scoring** — Calibrated to criminological sophistication indicators,
  not just technical confidence scores

---

## The Theory Behind It

**Routine Activity Theory (Cohen & Felson, 1979)**
Crime requires convergence of: motivated offender + suitable target +
absent guardian. Traditional security focuses on the last two.
Chronoscope profiles the first.

**Adversarial Chronotope**
The temporal-spatial relationship in attack patterns reveals operational
rhythm — professional actors have professional schedules.
Irregular actors show irregular patterns. The data confirms this.

**Criminal Behavioral Fingerprinting**
Infrastructure rotates. Behavior persists.
Chronoscope generates SHA-256 behavioral signatures that identify
actor consistency across changing infrastructure.

---

## Architecture

```
AbuseIPDB Live Feed
      ↓
Temporal Analysis Engine
      ↓
AdversarialChronotope (RAT Engine)
      ↓
Criminal Behavioral Fingerprinting
      ↓
Real-Time WebSocket Dashboard
```

**Stack:** FastAPI · WebSockets · SQLite · Docker · Python AsyncIO · AbuseIPDB

---

## Quick Start

```bash
git clone https://github.com/Unnathi-vithlani/chronoscope
cd chronoscope
cp .env.example .env        # Add your AbuseIPDB key (or leave DEMO_MODE=True)
docker-compose up
```

Then open: http://localhost:8000

Demo mode works immediately without an API key.

---

## Live Results

Running against AbuseIPDB live data:

| Finding | What the Data Shows |
|---------|-------------------|
| Professional actors (>90 confidence) | Cluster 6am–2pm UTC — consistent with organized professional operation |
| Low-sophistication actors | Wide temporal variance — consistent with opportunistic behavior |
| Infrastructure vs. behavior mismatch | Netherlands exit nodes showing Eastern European behavioral profiles |
| Behavioral signature persistence | Same fingerprints recur on different IPs across 48hr windows |

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Service status and stats |
| `GET /threats/live` | Latest criminal profiles |
| `GET /criminals/{id}` | Single criminal profile by fingerprint ID |
| `WS /ws/live` | Real-time WebSocket stream |

---

## About the Author

Built by **Unnathi Vithlani** — former cybercrime investigator (4.5 years,
law enforcement India), NSF research contributor (Award #2450046, SMU),
M.S. Cybersecurity (SMU, 3.84 GPA), M.A. Criminology, M.Com.

This project is the applied implementation of the following published research:
- "How Criminal Psychology Can Make Cybersecurity Teams More Effective"
- "The $10 Trillion Problem: Why Fighting Financial Cybercrime Requires a New Playbook"
- arXiv paper in preparation: "Behavioral Profiling of Cybercriminals: A Criminological Framework for Cyber Threat Intelligence"

---

## License

MIT — free to use, fork, and extend.
