# scripts/stop_control.ps1
$ErrorActionPreference = "Stop"
$pidFile = "data/control_api.pid"
if (-not (Test-Path $pidFile)) {
    Write-Output "No PID file found at $pidFile"
    exit 0
}
$pid = Get-Content $pidFile -Raw
try {
    Stop-Process -Id ([int]$pid) -Force -ErrorAction Stop
    Remove-Item -Force $pidFile -ErrorAction SilentlyContinue
    Write-Output "Stopped process $pid and removed PID file"
} catch {
    Write-Output "Failed to stop process $pid: $_"
}
