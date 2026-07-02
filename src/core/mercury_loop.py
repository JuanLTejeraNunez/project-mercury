import os
import json

# Mercury loop
# Runs the full cycle:
# 1. Generate opportunities
# 2. Review results
# 3. Create narrative analysis
# 4. Evaluate strategy
# 5. Apply controlled learning
# 6. Log everything
# 7. Repeat safely

def run_step(command):
    print("Running:", command)
    result = os.system(command)
    if result != 0:
        print("Error running:", command)
    else:
        print("Completed:", command)

def run_mercury_cycle():
    print("=== Mercury Full Cycle Start ===")

    # Step 1: Generate opportunities
    run_step("python export_mercury_json.py")

    # Step 2: Review results
    run_step("python review_results.py")

    # Step 3: Narrative analysis
    run_step("python analysis_narrative.py")

    # Step 4: Strategy evaluation
    run_step("python strategy_evaluator.py")

    # Step 5: Controlled learning
    run_step("python learning_module.py")

    print("=== Mercury Full Cycle Complete ===")

if __name__ == "__main__":
    run_mercury_cycle()
