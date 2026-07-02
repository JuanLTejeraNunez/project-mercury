from typing import List, Dict

class MercuryBankrollEngine:
    """
    Motor de bankroll:
    - evalÃºa resultados de mercados
    - calcula PnL
    - calcula bankroll final
    """

    def evaluate_results(self, allocations: List[Dict], outcomes: Dict[str, bool]):
        """
        allocations: lista con 'id' y 'stake'
        outcomes: dict {id: True/False}

        Retorna:
        {
            "final_bankroll": float,
            "details": [
                {"id": str, "stake": float, "won": bool, "pnl": float}
            ]
        }
        """

        bankroll = 0.0
        details = []

        for alloc in allocations:
            mid = alloc["id"]
            stake = alloc["stake"]
            won = outcomes.get(mid, False)

            if won:
                # Ejemplo simple: retorno 2x (stake + ganancia igual al stake)
                pnl = stake
                bankroll += stake + pnl
            else:
                pnl = -stake
                # bankroll no suma nada porque se pierde el stake

            details.append({
                "id": mid,
                "stake": stake,
                "won": won,
                "pnl": pnl,
            })

        return {
            "final_bankroll": bankroll,
            "details": details,
        }



