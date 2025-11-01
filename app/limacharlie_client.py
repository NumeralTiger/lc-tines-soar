import os
import requests
from typing import Dict

LC_API_BASE = "https://api.limacharlie.io/v1"

API_KEY = os.getenv("LIMACHARLIE_API_KEY")
if not API_KEY:
    raise EnvironmentError("LIMACHARLIE_API_KEY missing from env")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def isolate_sensor(sid: str, reason: str = "Automated containment via SOAR") -> Dict:
    """
    Call LimaCharlie POST /{sid}/isolation to place sensor into network isolation.
    Returns parsed JSON response or raises requests.HTTPError.
    """
    if not sid:
        raise ValueError("Sensor id (sid) is required")
    url = f"{LC_API_BASE}/{sid}/isolation"
    payload = {"reason": reason}
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json() if r.text else {"status": "ok"}

def rejoin_sensor(sid: str) -> Dict:
    """
    Example: call to rejoin/unisolate if desired (docs provide unisolate endpoint).
    Implementation left as similar to isolate_sensor if needed.
    """
    url = f"{LC_API_BASE}/{sid}/rejoin"  # placeholder if docs provide /rejoin; otherwise adapt
    r = requests.post(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json() if r.text else {"status": "ok"}

def get_sensor_info(sid: str) -> Dict:
    """Get sensor metadata (optional)."""
    url = f"{LC_API_BASE}/{sid}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()
