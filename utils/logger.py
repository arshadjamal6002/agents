import json
from datetime import datetime

def log_trace(name, input, output, passed=True):
    trace = {
        "name": name,
        "input": input,
        "output": output,
        "timestamp": str(datetime.now()),
        "status": "PASS" if passed else "FAIL"
    }

    with open(f"trace_outputs/{name}.json", "w") as f:
        json.dump(trace, f, indent=2)
