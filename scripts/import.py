#!/usr/bin/env python3
"""Import/update all workflows in workflows/ directory to n8n."""
import json, requests, os, sys, glob

N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
API_KEY = os.environ.get("N8N_API_KEY", "n8n_api_de166e5eb15c11245391ebd4af63b01e6bae4378")
HEADERS = {"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"}

# Map workflow name → existing ID (update in place)
existing = {w["name"]: w["id"] for w in requests.get(f"{N8N_URL}/api/v1/workflows", headers=HEADERS).json().get("data", [])}

for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "workflows", "*.json"))):
    with open(path) as f: wf = json.load(f)
    payload = {k: wf[k] for k in ["name","nodes","connections","settings"] if k in wf}
    name = wf.get("name", "?")
    if name in existing:
        resp = requests.put(f"{N8N_URL}/api/v1/workflows/{existing[name]}", headers=HEADERS, json=payload)
        print(f"{✅ if resp.ok else ❌} Updated: {name}")
    else:
        resp = requests.post(f"{N8N_URL}/api/v1/workflows", headers=HEADERS, json=payload)
        print(f"{✅ if resp.ok else ❌} Created: {name}")
