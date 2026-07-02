<#
    organize_mercury.ps1
    Script único para organizar Mercury:

      - Crear carpetas estándar si faltan
      - Mover scripts .ps1 a scripts/
      - Reubicar archivos .py clave desde la raíz a src/
      - Limpiar .pyc y .bak dentro de src/

    Ejecutar desde la raíz del proyecto:
      PS> .\organize_mercury.ps1
#>

# --- 1) Detectar raíz del proyecto ---
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Raíz detectada: $Root"
Set-Location $Root

# --- 2) Crear carpetas estándar ---
$requiredDirs = @(
    "src","scripts","configs","data","logs","history",
    "outputs","templates","tests","docs","infra","backups"
)

foreach ($dir in $requiredDirs) {
    $full = Join-Path $Root $dir
    if (-not (Test-Path $full)) {
        Write-Host "Creando carpeta: $dir"
        New-Item -ItemType Directory -Path $full | Out-Null
    }
}

# --- 3) Mover scripts .ps1 a scripts/ ---
Write-Host "`n== Moviendo scripts .ps1 a scripts/ =="

$scriptTarget = Join-Path $Root "scripts"

Get-ChildItem -Path $Root -Filter *.ps1 -File | ForEach-Object {
    if ($_.Name -ne "organize_mercury.ps1") {
        $dest = Join-Path $scriptTarget $_.Name
        Write-Host "Moviendo $($_.Name)"
        Move-Item -Path $_.FullName -Destination $dest -Force -ErrorAction SilentlyContinue
    }
}

# --- 4) Reubicar archivos .py clave ---
Write-Host "`n== Reubicando archivos .py desde la raíz a src/ =="

$srcBase = Join-Path $Root "src"

$pyMap = @{
    "analysis_agent.py" = "agents"
    "review_results.py" = "core"
    "run_agent.py"      = ""
    "run_mercury.py"    = ""
}

foreach ($entry in $pyMap.GetEnumerator()) {

    $fileName  = $entry.Key
    $subFolder = $entry.Value

    $sourcePath = Join-Path $Root $fileName

    if (Test-Path $sourcePath) {

        if ($subFolder -eq "") {
            $destDir = $srcBase
        } else {
            $destDir = Join-Path $srcBase $subFolder
            if (-not (Test-Path $destDir)) {
                Write-Host "Creando carpeta src/$subFolder"
                New-Item -ItemType Directory -Path $destDir | Out-Null
            }
        }

        $destPath = Join-Path $destDir $fileName

        Write-Host "Moviendo $fileName -> $destDir"
        Move-Item -Path $sourcePath -Destination $destPath -Force -ErrorAction SilentlyContinue
    }
}

# --- 5) Limpiar .pyc y .bak ---
Write-Host "`n== Limpiando *.pyc y *.bak dentro de src/ =="

Get-ChildItem -Path $srcBase -Recurse -Include *.pyc, *.bak -File -ErrorAction SilentlyContinue |
    ForEach-Object {
        Write-Host "Eliminando: $($_.FullName)"
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
    }

Write-Host "`n== Organización completada =="
Write-Host "Ejecuta: tree /F para verificar la nueva estructura."
