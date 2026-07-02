<#
    fix_providers.ps1
    Corrige:
      1. Añade get_markets_public a src/markets/kalshi.py
      2. Conecta esa función en src/providers/kalshi_client.py
      3. Arregla Polymarket (strings JSON → dicts)
#>

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "Corrigiendo Polymarket + Kalshi..."

# ============================================================
# 1. Añadir get_markets_public a src/markets/kalshi.py
# ============================================================

$kalshiMarketsPath = "src/markets/kalshi.py"

if (Test-Path $kalshiMarketsPath) {
    Write-Host "Actualizando $kalshiMarketsPath ..."

@"
# --- Añadido automáticamente por fix_providers.ps1 ---
def get_markets_public(limit: int = 200):
    \"\"\"
    Obtiene mercados públicos desde Kalshi sin autenticación.
    Usa la URL correcta de producción.
    \"\"\"
    import requests
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
# --- Fin de bloque añadido ---
"@ | Add-Content $kalshiMarketsPath
} else {
    Write-Host "ERROR: No existe src/markets/kalshi.py"
}

# ============================================================
# 2. Conectar get_markets_public en src/providers/kalshi_client.py
# ============================================================

$kalshiProviderPath = "src/providers/kalshi_client.py"

if (Test-Path $kalshiProviderPath) {
    Write-Host "Actualizando $kalshiProviderPath ..."

@"
# --- Añadido automáticamente por fix_providers.ps1 ---
from src.markets.kalshi import get_markets_public

def get_markets_raw(self):
    try:
        markets = get_markets_public()
        logging.info(f"[KalshiClient] Recibidos {len(markets)} mercados públicos desde Kalshi.")
        return markets
    except Exception as e:
        logging.error(f"[KalshiClient] Error al obtener mercados: {e}")
        return []
# --- Fin de bloque añadido ---
"@ | Add-Content $kalshiProviderPath
} else {
    Write-Host "ERROR: No existe src/providers/kalshi_client.py"
}

# ============================================================
# 3. Arreglar Polymarket (strings JSON → dicts)
# ============================================================

$polyPath = "src/providers/polymarket_client.py"

if (Test-Path $polyPath) {
    Write-Host "Corrigiendo Polymarket en $polyPath ..."

@"
# --- Añadido automáticamente por fix_providers.ps1 ---
import json

def get_markets_raw(self):
    try:
        resp = requests.get(self.api_url, timeout=10)
        resp.raise_for_status()
        raw = resp.json()

        markets = []
        for item in raw:
            if isinstance(item, str):
                markets.append(json.loads(item))
            else:
                markets.append(item)

        logging.info(f"[PolymarketClient] Recibidos {len(markets)} mercados crudos (normalizados).")
        return markets

    except Exception as e:
        logging.error(f"[PolymarketClient] Error al obtener mercados: {e}")
        return []
# --- Fin de bloque añadido ---
"@ | Add-Content $polyPath
} else {
    Write-Host "ERROR: No existe src/providers/polymarket_client.py"
}

# ============================================================
# Git commit + push
# ============================================================

Write-Host "Realizando commit y push..."
git add .
git commit -m "Fix: Polymarket JSON strings, Kalshi public markets integration"
git push

Write-Host "Correcciones completadas."
