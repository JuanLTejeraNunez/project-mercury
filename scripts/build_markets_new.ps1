Write-Host "Generando mercados combinados (Polymarket + Kalshi)..."

$project = "C:\Users\jltej\project-mercury"
$python = "$project\.venv\Scripts\python.exe"
$env:PYTHONPATH = "$project"

& $python -m src.markets.build_markets

Write-Host "Mercados generados correctamente."
