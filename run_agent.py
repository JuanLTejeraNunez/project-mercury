import time
from datetime import datetime, timedelta

from src.agents.analysis_agent import MercuryAnalysisAgent


def run_agent(duration_hours=24, initial_bankroll=100.0, reinvest_rate=0.40):
    """
    Ejecuta el agente Mercury durante un periodo real de tiempo.
    No usa simulacion. Solo datos reales de Polymarket.
    """

    agent = MercuryAnalysisAgent(
        initial_bankroll=initial_bankroll,
        reinvest_rate=reinvest_rate
    )

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)

    print("Mercury Agent iniciado")
    print("Inicio:", start_time)
    print("Fin esperado:", end_time)
    print("Bankroll inicial:", initial_bankroll)
    print("Reinvest rate:", reinvest_rate)
    print("----------------------------------------")

    cycle_number = 1
    history = []

    while datetime.now() < end_time:
        print(f"\nCiclo {cycle_number} ejecutandose...")

        result = agent.run_cycle()

        allocations = result["allocations"]
        pnl_result = result["pnl_result"]
        learning = result["learning"]
        new_bankroll = result["new_bankroll"]

        print("Bankroll despues del ciclo:", new_bankroll)
        print("Accuracy:", learning["accuracy"])
        print("Brier score:", learning["brier_score"])

        history.append({
            "cycle": cycle_number,
            "bankroll": new_bankroll,
            "accuracy": learning["accuracy"],
            "brier": learning["brier_score"],
            "pnl": pnl_result["final_bankroll"]
        })

        cycle_number += 1

        # Espera real entre ciclos
        time.sleep(10)

    print("\n----------------------------------------")
    print("Mercury Agent finalizado")
    print("Ciclos ejecutados:", cycle_number - 1)
    print("Bankroll final:", agent.bankroll)
    print("----------------------------------------")

    return history


if __name__ == "__main__":
    # Ejecuta el agente por 24 horas con bankroll inicial de 100
    history = run_agent(
        duration_hours=24,
        initial_bankroll=100.0,
        reinvest_rate=0.40
    )

    print("\nHistorial completo:")
    for h in history:
        print(h)

