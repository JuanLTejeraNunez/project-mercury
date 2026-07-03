# scripts/clear_stop_worker.ps1
# Removes the stop flag file
if (Test-Path data\stop_worker) {
    Remove-Item -Force data\stop_worker
    Write-Output "Removed data\stop_worker"
} else {
    Write-Output "No stop flag present"
}
