# Decision Flow: instrucciones rápidas

**Archivos añadidos/actualizados**
- src/core/bet_manager.py  (mejorado: soporta decision_reason, expected_roi, time_horizon, stake_requested, decision_metadata)
- src/control/api.py      (API con token y endpoints: /submit_decision, /decisions, /approve_decision, /force_check, /bets, /status, /stop, /start)
- scripts/agent_submit_decision.py  (ejemplo: el agente envía una Decision Card)
- scripts/approve_decision.ps1      (aprobación desde PowerShell)
- .env (si usaste el script anterior) o exporta CONTROL_API_TOKEN en tu entorno

**Pruebas rápidas**
1. Establece token de control:
   - En PowerShell: $env:CONTROL_API_TOKEN = "tu_token_secreto"
   - O crea .env con CONTROL_API_TOKEN=<token> y exporta antes de arrancar uvicorn.

2. Arranca la API (en esta sesión con venv activado):
   python -m uvicorn control.api:app --host 127.0.0.1 --port 8000 --reload

3. Simula agente (envía Decision Card):
   python scripts/agent_submit_decision.py --token <TOKEN>

4. Lista decisiones:
   Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/decisions -Headers @{ Authorization = "Bearer <TOKEN>" }

5. Aprueba una decisión (desde PowerShell):
   .\scripts\approve_decision.ps1 -Token "<TOKEN>" -DecisionId "<decision-id>" -Stake 5 -ExpectedClose "2026-07-10T18:00:00Z"

6. Forzar comprobación:
   Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/force_check -Headers @{ Authorization = "Bearer <TOKEN>" }

**Notas**
- El flujo separa la **decisión** (submit_decision) de la **ejecución** (approve_decision). Esto obliga a que un operador revise y apruebe stake y expected_close antes de abrir la apuesta.
- decision_metadata guarda señales y timestamps para auditoría.
- En producción, protege el token y usa Docker secrets o un gestor de secretos.
