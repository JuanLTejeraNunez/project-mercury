"""
SIMULATION DISABLED
Este archivo ha sido desactivado automáticamente.
Mercury ahora trabaja SOLO con datos reales.
"""

# """ from typing import List, Dict
# 
# class MercurySimulationEngine:
#     """
#     Motor de cálculo basado en datos reales.
#     No simula nada: solo calcula métricas reales.
#     """
# 
#     def calculate_pnl(self, allocations: List[Dict], outcomes: Dict[str, bool]):
#         """
#         Calcula PnL real basado en resultados reales.
#         - allocations: lista de dicts con keys "id" y "stake"
#         - outcomes: dict mapping id -> bool (True si ganó)
#         Devuelve: dict con keys "pnl" y "win_rate"
#         """
#         pnl = 0.0
#         wins = 0
# 
#         for alloc in allocations:
#             mid = alloc["id"]
#             stake = alloc["stake"]
#             won = outcomes.get(mid, False)
# 
#             if won:
#                 pnl += stake
#                 wins += 1
#             else:
#                 pnl -= stake
# 
#         win_rate = wins / len(allocations) if allocations else 0.0
# 
#         return {
#             "pnl": pnl,
#             "win_rate": win_rate
#         }
# 
#     def simulate_binary_events(self, probs, trials: int = 1, rng_seed: int | None = None):
#         """
#         Simula eventos binarios y devuelve una lista plana de 0/1 con longitud len(probs)*trials.
#         Acepta probabilidades en 0..1 o 0..100. rng_seed opcional para reproducibilidad.
#         """
#         try:
#             from random import Random
#         except Exception:
#             import random as _random
#             Random = _random.Random
# 
#         rng = Random(rng_seed) if rng_seed is not None else Random()
#         flat = []
#         for p in probs:
#             if p is None:
#                 p = 0.0
#             if p > 1 and p <= 100:
#                 p = p / 100.0
#             p = max(0.0, min(1.0, float(p)))
#             for _ in range(int(trials)):
#                 flat.append(1 if rng.random() < p else 0)
#         return flat
# 
#     def simulate_pnl(self, probs, stake: float = 1.0, rng_seed: int | None = None):
#         """
#         Calcula/simula PnL por cada probabilidad en `probs` y devuelve {'pnl': [...], 'win_rate': float}.
#         - Intenta usar self.calculate_pnl(prob, stake, outcome) si existe; si no, usa stake*(2*prob-1).
#         - win_rate se calcula como la fracción de outcomes simulados que resultaron en 1.
#         """
#         has_calc = hasattr(self, "calculate_pnl") and callable(getattr(self, "calculate_pnl"))
#         try:
#             from random import Random
#         except Exception:
#             import random as _random
#             Random = _random.Random
#         rng = Random(rng_seed) if rng_seed is not None else Random()
# 
#         pnls = []
#         wins = 0
#         total = 0
#         for p in probs:
#             if p is None:
#                 p = 0.0
#             if p > 1 and p <= 100:
#                 p = p / 100.0
#             p = max(0.0, min(1.0, float(p)))
# 
#             # Simulamos outcome para poder calcular win_rate de forma consistente
#             outcome = 1 if rng.random() < p else 0
#             total += 1
#             wins += outcome
# 
#             if has_calc:
#                 try:
#                     pnl = self.calculate_pnl(p, stake, outcome)
#                 except TypeError:
#                     try:
#                         pnl = self.calculate_pnl(p, stake)
#                     except Exception:
#                         pnl = stake * (2 * p - 1)
#                 except Exception:
#                     pnl = stake * (2 * p - 1)
#             else:
#                 pnl = stake * (2 * p - 1)
# 
#             pnls.append(float(pnl))
# 
#         win_rate = (wins / total) if total > 0 else 0.0
#         return {"pnl": pnls, "win_rate": win_rate}
# """


