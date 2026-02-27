import json
import os
import subprocess
subprocess.run(["pip", "install", "requests", "-q"], check=True)
import requests

# Read workflow information from environment (set defaults if missing)
workflow_name = os.getenv("WORKFLOW_NAME", "UNKNOWN_WORKFLOW")
workflow_status = os.getenv("WORKFLOW_STATUS", "UNKNOWN_STATUS")

# Build payload first
config = {
    "model": "tinyllama",
    "prompt": f"Workflow {workflow_name} finished with status {workflow_status}. Provide a brief plain English summary of what likely went wrong and suggest next steps.",
    "stream": False,
}

# Primary attempt: use requests
try:
    response = requests.post(
        "http://ollama-svc:11434/api/generate",
        json=config,
        timeout=10,
    )
    response.raise_for_status()
    result = response.json()
    print("Summary of root analysis:")
    print(result.get("response", "No text found in response"))
except Exception as e:
    print("requests POST failed:", e)
    # Fallback: use curl via subprocess
    try:
        cp = subprocess.run([
            "curl",
            "-sS",
            "-X",
            "POST",
            "http://ollama-svc:11434/api/generate",
            "-H",
            "Content-Type: application/json",
            "-d",
            json.dumps(config),
        ], capture_output=True, text=True)
        if cp.returncode == 0:
            result = json.loads(cp.stdout)
            print("Summary of root analysis (curl):")
            print(result.get("response", "No text found in response"))
        else:
            print(f"curl failed: returncode {cp.returncode}")
            print("stderr:", cp.stderr)
    except Exception as e2:
        print("curl fallback failed:", e2)