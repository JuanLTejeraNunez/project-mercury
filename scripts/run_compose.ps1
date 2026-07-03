# scripts/run_compose.ps1
$ErrorActionPreference = "Stop"
param(
    [string]$Token = $(Read-Host "CONTROL_API_TOKEN (enter token to set for compose)")
)
if (-not $Token) {
    Write-Output "No token provided; aborting."
    exit 1
}
$env:CONTROL_API_TOKEN = $Token
docker-compose up -d --build
Write-Output "Started docker-compose stack (control_api + agent)."
