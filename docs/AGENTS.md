# Sistema de Agentes Hermes

Hermes está compuesto por múltiples agentes internos:

## CoordinatorAgent
- Orquesta el sistema
- Decide qué agente debe actuar
- Maneja el flujo de tareas

## MemoryAgent
- Guarda y recupera información
- Interactúa con SQLite
- Mantiene contexto persistente

## TaskAgent
- Ejecuta tareas operativas
- Procesa instrucciones del usuario

## AnalysisAgent
- Realiza análisis complejos
- Procesa datos y genera conclusiones

## Futuras extensiones
- WebAgent
- FileAgent
- PlanningAgent
