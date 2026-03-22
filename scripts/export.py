#!/usr/bin/env python3
"""Export all active n8n workflows to workflows/ directory."""
import json, requests, re, os, sys

N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
API_KEY = os.environ.get("N8N_API_KEY", "n8n_api_de166e5eb15c11245391ebd4af63b01e6bae4378")
HEADERS = {"X-N8N-API-KEY": API_KEY}
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "workflows")

os.makedirs(OUT_DIR, exist_ok=True)
resp = requests.get(f"{N8N_URL}/api/v1/workflows", headers=HEADERS)
workflows = resp.json().get("data", [])
for wf in workflows:
    if wf.get("isArchived"): continue
    wf_id = wf["id"]
    detail = requests.get(f"{N8N_URL}/api/v1/workflows/{wf_id}", headers=HEADERS).json()
    out = {k: detail[k] for k in ["name","nodes","connections","settings"] if k in detail}
    slug = re.sub(r"[^a-z0-9]+", "-", detail["name"].lower()).strip("-")[:50]
    path = os.path.join(OUT_DIR, f"{slug}.json")
    with open(path, "w") as f: json.dump(out, f, indent=2)
    print(f"✅  {detail[name]} → {slug}.json")
