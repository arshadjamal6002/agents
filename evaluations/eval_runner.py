import yaml
import json
from orchestrator_agent import handle_user_input
from datetime import datetime
from pathlib import Path

TRACE_DIR = Path("trace_outputs")
TRACE_DIR.mkdir(exist_ok=True)

def run_eval():
    with open("evaluations/tests.yaml") as f:
        tests = yaml.safe_load(f)["tests"]

    for test in tests:
        print(f"Running test: {test['name']}")
        output = handle_user_input(test["input"])
        result_text = json.dumps(output)

        passed = test["expected_contains"].lower() in result_text.lower()
        print(f"✅ PASSED" if passed else "❌ FAILED")

        # Save trace
        trace_path = TRACE_DIR / f"{test['name'].replace(' ', '_')}.json"
        with open(trace_path, "w") as f:
            json.dump({
                "test": test,
                "output": output,
                "passed": passed,
                "timestamp": str(datetime.now())
            }, f, indent=2)

if __name__ == "__main__":
    run_eval()
