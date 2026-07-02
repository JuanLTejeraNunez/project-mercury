# Crear carpetas
New-Item -ItemType Directory -Path "src/knowledge" -Force | Out-Null
New-Item -ItemType Directory -Path "src/knowledge/baseball" -Force | Out-Null
# Crear archivos vacios
New-Item -ItemType File -Path "src/knowledge/baseball/__init__.py" -Force | Out-Null
New-Item -ItemType File -Path "src/knowledge/baseball/baseball_api_mlb.py" -Force | Out-Null
New-Item -ItemType File -Path "src/knowledge/baseball/baseball_api_espn.py" -Force | Out-Null
New-Item -ItemType File -Path "src/knowledge/baseball/baseball_api_fangraphs.py" -Force | Out-Null
New-Item -ItemType File -Path "src/knowledge/baseball/baseball_knowledge.py" -Force | Out-Null
# Copiar plantillas
Copy-Item "templates/baseball_api_mlb.txt" "src/knowledge/baseball/baseball_api_mlb.py" -Force
Copy-Item "templates/baseball_api_espn.txt" "src/knowledge/baseball/baseball_api_espn.py" -Force
Copy-Item "templates/baseball_api_fangraphs.txt" "src/knowledge/baseball/baseball_api_fangraphs.py" -Force
Copy-Item "templates/baseball_knowledge.txt" "src/knowledge/baseball/baseball_knowledge.py" -Force
