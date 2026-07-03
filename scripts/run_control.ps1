# scripts/run_control.ps1
$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Resolve-Path src).Path
& ".\.venv\Scripts\Activate.ps1"

# Ensure dependencies
python -m pip install --upgrade pip setuptools wheel | Out-Null
python -m pip install fastapi uvicorn | Out-Null

# PID file location
$pidFile = "data/control_api.pid"
# If already running, warn
if (Test-Path $pidFile) {
    try {
        $existingPid = Get-Content $pidFile -Raw
        Write-Output "PID file exists: $existingPid. Check if process is alive before starting another instance."
    } catch {}
}

# Start uvicorn in background and write PID
$uvicornArgs = @("-m","uvicorn","control.api:app","--host","127.0.0.1","--port","8000","--log-level","info","--reload")
$proc = Start-Process -FilePath python -ArgumentList $uvicornArgs -PassThru
Start-Sleep -Seconds 1
$proc.Id | Out-File -Encoding ascii $pidFile -Force
Write-Output "Started control API (uvicorn) with PID $($proc.Id). PID file: $pidFile"
Write-Output "Access the API at http://127.0.0.1:8000"
