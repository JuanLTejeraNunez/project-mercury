<#
    fix_imports.ps1
    Corrige:
      - Import incorrecto en kalshi_client.py
      - Falta de import requests en polymarket_client.py
#>

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "Corrigiendo imports en Kalshi y Polymarket..."

# ============================================================
# 1. Corregir import en src/providers/kalshi_client.py
# ============================================================

$kalshiProviderPath = "src/providers/kalshi_client.py"

if (Test-Path $kalshiProviderPath) {
    Write-Host "Corrigiendo import en $kalshiProviderPath ..."

    (Get-Content $kalshiProviderPath) `
        -replace "from src.markets.kalshi import get_markets_public", "from markets.kalshi import get_markets_public" `
        | Set-Content $kalshiProviderPath
} else {
    Write-Host "ERROR: No existe src/providers/kalshi_client.py"
}

# ============================================================
# 2. Añadir import requests en Polymarket si falta
# ============================================================

$polyPath = "src/providers/polymarket_client.py"

if (Test-Path $polyPath) {
    Write-Host "Corrigiendo Polymarket imports en $polyPath ..."

    $content = Get-Content $polyPath

    if ($content -notcontains "import requests") {
        Write-Host "Añadiendo 'import requests'..."
        @"
import requests
"@ | Add-Content $polyPath
    }
} else {
    Write-Host "ERROR: No existe src/providers/polymarket_client.py"
}

# ============================================================
# Git commit + push
# ============================================================

Write-Host "Realizando commit y push..."
git add .
git commit -m "Fix: corrected imports for Kalshi and Polymarket providers"
git push

Write-Host "Correcciones completadas."
