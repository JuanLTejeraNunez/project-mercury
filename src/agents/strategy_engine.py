from typing import List, Dict

class MercuryStrategyEngine:
    """
    Motor de estrategia:
    - recibe mercados con probabilidad estimada
    - decide pesos relativos del bankroll
    """

    def allocate_bankroll(self, markets: List[Dict], bankroll: float = 100.0):
        """
        Recibe una lista de mercados con campo 'prob' y reparte el bankroll.
        Estrategia simple: proporcional a probabilidad.
        """
        if not markets:
            return []

        total_prob = sum(m["prob"] for m in markets)
        if total_prob == 0:
            raise ValueError("La suma de probabilidades no puede ser 0.")

        allocations = []
        for m in markets:
            weight = m["prob"] / total_prob
            stake = bankroll * weight
            allocations.append({
                "id": m["id"],
                "question": m.get("question", ""),
                "prob": m["prob"],
                "weight": weight,
                "stake": stake,
            })
        return allocations



