<#
    fix_kalshi_full.ps1
    Reemplaza completamente src/markets/kalshi.py con una versión limpia y funcional.
#>

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$kalshiPath = "src/markets/kalshi.py"

Write-Host "Reemplazando archivo completo: $kalshiPath ..."

@"
import os
import time
import json
import base64
from typing import Dict, Any, Optional
import requests

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# URL correcta para mercados públicos
BASE_URL = os.getenv("KALSHI_BASE_URL", "https://api.elections.kalshi.com/trade-api/v2")
API_KEY_ID = os.getenv("KALSHI_API_KEY_ID")
PRIVATE_KEY_PEM = os.getenv("KALSHI_PRIVATE_KEY")
PRIVATE_KEY_PATH = os.getenv("KALSHI_PRIVATE_KEY_PATH")

DEFAULT_TIMEOUT = 8
RETRY_BACKOFF = [0.5, 1.0, 2.0]

def _load_private_key_from_env_or_path():
    pem = None
    if PRIVATE_KEY_PEM:
        pem = PRIVATE_KEY_PEM
    elif PRIVATE_KEY_PATH:
        try:
            with open(PRIVATE_KEY_PATH, "r", encoding="utf-8") as f:
                pem = f.read()
        except Exception:
            pem = None
    if not pem:
        return None
    return serialization.load_pem_private_key(pem.encode("utf-8"), password=None)

def _sign_request(private_key, timestamp: str, method: str, path: str, body: Optional[str]):
    msg = timestamp + method.upper() + path + (body or "")
    signature = private_key.sign(
        msg.encode("utf-8"),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")

def _request_with_retries(method: str, path: str, json_body: Optional[dict] = None, params: Optional[dict] = None):
    url = BASE_URL.rstrip("/") + path
    body_text = json.dumps(json_body) if json_body is not None else ""
    ts = str(int(time.time() * 1000))
    pk = _load_private_key_from_env_or_path()
    signature = _sign_request(pk, ts, method, path, body_text) if pk else ""
    headers = {
        "KALSHI-ACCESS-KEY": API_KEY_ID or "",
        "KALSHI-ACCESS-SIGNATURE": signature,
        "KALSHI-ACCESS-TIMESTAMP": ts,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    last_exc = None
    for delay in RETRY_BACKOFF:
        try:
            resp = requests.request(method, url, headers=headers, timeout=DEFAULT_TIMEOUT, json=json_body, params=params)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc

def get_market_probability(market_id: str) -> float:
    try:
        resp = _request_with_retries("GET", f"/markets/{market_id}")
    except Exception:
        resp = _request_with_retries("GET", "/markets", params={"ticker": market_id, "limit": 1})
    data = resp.json()
    if isinstance(data, dict) and "market" in data:
        m = data["market"]
    elif isinstance(data, dict) and "markets" in data:
        markets = data.get("markets") or []
        m = markets[0] if markets else {}
    else:
        m = data if isinstance(data, dict) else {}
    price = m.get("midpoint") or m.get("price") or m.get("last_price") or m.get("probability") or 0.0
    try:
        p = float(price)
    except Exception:
        p = 0.0
    return max(0.0, min(1.0, p))

def place_order(ticker: str, side: str, count: float, price: float, client_order_id: str) -> Dict[str, Any]:
    if not API_KEY_ID:
        raise RuntimeError("KALSHI_API_KEY_ID no configurado; no se puede colocar orden.")
    pk = _load_private_key_from_env_or_path()
    if not pk:
        raise RuntimeError("Clave privada no disponible; configure KALSHI_PRIVATE_KEY_PATH o KALSHI_PRIVATE_KEY.")
    payload = {
        "ticker": ticker,
        "side": side,
        "count": count,
        "price": price,
        "client_order_id": client_order_id,
    }
    resp = _request_with_retries("POST", "/portfolio/events/orders", json_body=payload)
    return resp.json()

# --- NUEVA FUNCIÓN LIMPIA ---
def get_markets_public(limit: int = 200):
    """
    Obtiene mercados públicos desde Kalshi sin autenticación.
    """
    url = "https://api.elections.kalshi.com/trade-api/v2/markets"
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and "markets" in data:
            return data["markets"][:limit]

        return data
    except Exception as e:
        print("[Kalshi] Error obteniendo mercados públicos:", e)
        return []
"@ | Set-Content $kalshiPath

Write-Host "Archivo reemplazado correctamente."
