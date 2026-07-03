# CONTROL_API_TOKEN

**Token generado:**  
$CONTROL_API_TOKEN (guárdalo en un lugar seguro)

**Valor (no compartas):**

**Uso rápido**
- El archivo .env en la raíz del repo contiene CONTROL_API_TOKEN.
- Para llamadas HTTP: Authorization: Bearer <TOKEN>.
- Para detener el stack: .\scripts\stop_compose.ps1 o docker compose down.

**Nota de seguridad:** este token se guarda en texto plano para conveniencia de pruebas. En producción usa Docker secrets o un gestor de secretos.
