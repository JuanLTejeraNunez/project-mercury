import time
import json
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
            "timestamp": datetime.now().isoformat(),
            "bankroll": new_bankroll,
            "accuracy": learning["accuracy"],
            "brier": learning["brier_score"],
            "pnl": pnl_result["final_bankroll"],
            "allocations": allocations,
        })

        cycle_number += 1

        # Espera real entre ciclos
        time.sleep(10)

    print("\n----------------------------------------")
    print("Mercury Agent finalizado")
    print("Ciclos ejecutados:", cycle_number - 1)
    print("Bankroll final:", agent.bankroll)
    print("----------------------------------------")

    # Guardar historial en archivo JSON
    log_path = "logs/mercury_history.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Historial guardado en: {log_path}")

    return history


if __name__ == "__main__":
    history = run_agent(
        duration_hours=24,
        initial_bankroll=100.0,
        reinvest_rate=0.40
    )

    print("\nHistorial completo (resumen):")
    for h in history:
        print(
            f"Ciclo {h['cycle']} | bankroll={h['bankroll']} | "
            f"accuracy={h['accuracy']} | brier={h['brier']}"
        )


