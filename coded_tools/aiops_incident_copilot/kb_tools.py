"""Grounding tools for the AIOps Incident Copilot (synthetic data only)."""
import json
import os
from typing import Any, Dict, List

from neuro_san.interfaces.coded_tool import CodedTool

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load(name: str) -> List[Dict[str, Any]]:
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def _search(items: List[Dict[str, Any]], query: str, top: int = 3) -> List[Dict[str, Any]]:
    words = [w for w in query.lower().replace(",", " ").split() if len(w) > 2]
    scored = []
    for item in items:
        text = json.dumps(item).lower()
        score = sum(text.count(w) for w in words)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in scored[:top]]


class CmdbLookup(CodedTool):
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Any:
        name = str(args.get("ci_name", "")).lower().strip()
        for ci in _load("cmdb.json"):
            if ci["ci_name"].lower() == name or name in ci["ci_name"].lower():
                return ci
        return {"result": f"CI '{name}' not found in CMDB"}


class IncidentHistorySearch(CodedTool):
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Any:
        hits = _search(_load("incident_history.json"), str(args.get("query", "")))
        return hits or {"result": "No similar past incidents found"}


class RunbookLookup(CodedTool):
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Any:
        hits = _search(_load("runbooks.json"), str(args.get("query", "")), top=2)
        return hits or {"result": "No approved runbook found - escalate to L3"}
