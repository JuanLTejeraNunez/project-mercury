# setup_secrets.ps1
if (-Not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item .env.example .env
        Write-Host ".env creado desde .env.example. Edita .env para añadir tus API keys (NO commitees .env)."
    } else {
        Write-Host "No se encontró .env.example. Crea .env manualmente con las variables necesarias."
    }
} else {
    Write-Host ".env ya existe. Editalo para añadir tus API keys."
}
Write-Host ""
Write-Host "Para cargar las variables en la sesión actual de PowerShell (temporal), ejecuta EXACTAMENTE:"
Write-Host "  Get-Content .env | ForEach-Object { if ($_ -match '^(?<k>\w+)=(.*)$') { Set-Item -Path \"Env:$($matches['k'])\" -Value $matches[2] } }"
