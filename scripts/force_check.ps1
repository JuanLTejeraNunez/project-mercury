# scripts/force_check.ps1
$ErrorActionPreference = "Stop"
$env:PYTHONPATH = (Resolve-Path src).Path
& ".\.venv\Scripts\Activate.ps1"

# Create a temporary Python file and run it
$temp = "temp_force_check.py"
$py = @"
from core.bet_manager import BetManager
bm = BetManager()
print("Open bets count:", len(bm.list_open_bets()))
bm._check_due_bets_once()
print("Forced check executed")
"@
$py | Out-File -Encoding utf8 $temp -Force

try {
    python $temp 2>&1 | ForEach-Object { Write-Output $_ }
} finally {
    Remove-Item -Force $temp -ErrorAction SilentlyContinue
}
