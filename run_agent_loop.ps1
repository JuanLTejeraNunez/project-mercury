# run_agent_loop.ps1
# Ejecuta analysis_agent.py en bucle. Ajusta AGENT_LOOP_INTERVAL en .env si quieres cambiar intervalo (segundos).
$venvActivate = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) { . $venvActivate } else { Write-Host "Advertencia: no se encontró venv en .venv." }
if (Test-Path ".env") {
    Get-Content .env | ForEach-Object { if ($_ -match "^(?<k>\w+)=(.*)$") { Set-Item -Path "Env:$($matches['k'])" -Value $matches[2] } }
}
if (-Not (Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
$interval = 60
if ($Env:AGENT_LOOP_INTERVAL) { $interval = [int]$Env:AGENT_LOOP_INTERVAL }
Write-Host "Starting agent loop. Interval = $interval s. DRY_RUN = $Env:DRY_RUN"
while ($true) {
    try {
        python -u analysis_agent.py 2>&1 | Tee-Object -FilePath "logs/agent_$(Get-Date -Format yyyyMMdd).log" -Append
    } catch {
        Write-Host "Error running analysis_agent.py: $_"
    }
    Start-Sleep -Seconds $interval
}
