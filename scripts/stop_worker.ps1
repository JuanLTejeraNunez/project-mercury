# scripts/stop_worker.ps1
# Creates the stop flag file so running BetManager worker will stop on next iteration
New-Item -ItemType File -Force -Path data\stop_worker | Out-Null
Write-Output "Created data\stop_worker flag. Worker will stop on next iteration."
