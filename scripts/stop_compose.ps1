# scripts/stop_compose.ps1
$ErrorActionPreference = "Stop"
docker-compose down
Write-Output "Stopped docker-compose stack."
