<#
    fix_kalshi_syntax.ps1
    Corrige el bloque mal insertado en src/markets/kalshi.py
    Reinstala get_markets_public() con sintaxis válida
#>

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$kalshiPath = "src/markets/kalshi.py"

if (-not (Test-Path $kalshiPath)) {
    Write-Host "ERROR: No existe src/markets/kalshi.py"
    exit
}

Write-Host "Corrigiendo sintaxis en $kalshiPath ..."

# 1. Eliminar cualquier bloque previo de get_markets_public
(Get-Content $kalshiPath) |
    Where-Object {$_ -notmatch "get_markets_public"} |
    Set-Content $kalshiPath

# 2. Insertar la versión correcta al final del archivo
@"
# --- get_markets_public añadido correctamente ---
def get_markets_public(limit: int = 200):
    \"\"\"
    Obtiene mercados públicos desde Kalshi sin autenticación.
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
# --- Fin de bloque ---
"@ | Add-Content $kalshiPath

Write-Host "Corrigiendo import en kalshi_client.py ..."

$kalshiClientPath = "src/providers/kalshi_client.py"

(Get-Content $kalshiClientPath) `
    -replace "from src.markets.kalshi import get_markets_public", "from markets.kalshi import get_markets_public" `
    | Set-Content $kalshiClientPath

Write-Host "Corrección completada."
