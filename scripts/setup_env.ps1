python -m venv .venv
. .venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install pandas pyarrow fastapi uvicorn numpy
Write-Output "Virtualenv created. Activate with: . .venv\\Scripts\\Activate.ps1"
