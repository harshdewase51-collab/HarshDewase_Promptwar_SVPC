import subprocess
import time
import requests
import json
import os
import sys

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BACKEND_DIR, ".env")
ENV_BACKUP = os.path.join(BACKEND_DIR, ".env.test_backup")
BASE_URL = "http://127.0.0.1:8000/api/v1"

def read_env():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_env(content):
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def set_env_key(key_value):
    content = read_env()
    lines = content.splitlines()
    new_lines = []
    found = False
    for line in lines:
        if line.startswith("AI_API_KEY="):
            new_lines.append(f"AI_API_KEY={key_value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"AI_API_KEY={key_value}")
    write_env("\n".join(new_lines) + "\n")

def start_backend():
    # Kill any process on 8000
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=1)
        if r.status_code == 200:
            pass
    except Exception:
        pass
    
    # Start uvicorn
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for ready
    for _ in range(30):
        time.sleep(0.5)
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=1)
            if r.status_code == 200:
                print(f"[+] Backend successfully started (PID: {proc.pid})")
                return proc
        except Exception:
            pass
    print("[-] Backend failed to start in time!")
    return proc

def stop_backend(proc):
    if proc:
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        except Exception:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                proc.kill()
        print("[+] Backend stopped")
        time.sleep(1)

def run_test():
    print("==================================================")
    print("STEP 1: Inspect AI Configuration")
    print("==================================================")
    orig_env = read_env()
    provider = "groq"
    model = "llama-3.3-70b-versatile"
    for line in orig_env.splitlines():
        if line.startswith("AI_PROVIDER="):
            provider = line.split("=", 1)[1].strip()
        if line.startswith("AI_MODEL="):
            model = line.split("=", 1)[1].strip()
    print(f"Provider: {provider}")
    print(f"Model: {model}")

    # Ensure backup
    if not os.path.exists(ENV_BACKUP):
        with open(ENV_BACKUP, "w", encoding="utf-8") as f:
            f.write(orig_env)
        print("[+] Created backup of .env")

    invalid_key = "gsk_invalid_test_key_fake1234567890abcdef"
    print(f"\n==================================================")
    print("STEP 2 & 3: Override AI_API_KEY with Invalid Key")
    print("==================================================")
    set_env_key(invalid_key)
    print(f"[+] AI_API_KEY set to: {invalid_key[:10]}...")

    print("\n==================================================")
    print("STEP 4 & 5: Start Backend with Invalid Key")
    print("==================================================")
    backend_proc = start_backend()

    results = {}
    try:
        print("\n==================================================")
        print("STEP 6: Send Real Analysis Request with Valid Payload")
        print("==================================================")
        payload = {
            "decision": "Accept a 6-month startup internship instead of completing my university semester on schedule.",
            "context": "Senior computer science student with 2 semesters remaining. The startup has 4 engineers. Monthly stipend is $3,500.",
            "reasoning": "The stipend is good and having real-world startup experience on my resume will guarantee higher-paying job offers later regardless of my graduation date."
        }
        resp = requests.post(f"{BASE_URL}/analysis", json=payload, timeout=20)
        print(f"HTTP Status: {resp.status_code}")
        print(f"Response Body: {resp.text}")

        # Check conditions
        # 1. Controlled error response
        is_controlled_error = False
        try:
            resp_json = resp.json()
            if not resp_json.get("success") and resp.status_code in [502, 500, 503]:
                is_controlled_error = True
        except Exception:
            pass
        results["controlled_error"] = is_controlled_error
        print(f"[CHECK] Controlled error response (HTTP 502/error format): {'PASS' if is_controlled_error else 'FAIL'}")

        # 2. Friendly error
        friendly_error = False
        if is_controlled_error:
            msg = resp_json.get("message") or resp_json.get("error", {}).get("message") or ""
            if "temporarily unavailable" in msg.lower() or "please try again" in msg.lower() or "error" in msg.lower():
                friendly_error = True
        results["friendly_error"] = friendly_error
        print(f"[CHECK] Friendly error message: {'PASS' if friendly_error else 'FAIL'} ('{msg if is_controlled_error else ''}')")

        # 3. Secret protection
        secret_leaked = (
            invalid_key in resp.text
            or "fake1234567890abcdef" in resp.text
            or "gsk_" in resp.text
            or "dev_secret_key" in resp.text
        )
        results["secret_protection"] = not secret_leaked
        print(f"[CHECK] Secret protection (no key leaked): {'PASS' if not secret_leaked else 'FAIL'}")

        # 4. No Python traceback exposed
        traceback_exposed = (
            "Traceback (most recent call last)" in resp.text
            or 'File "' in resp.text
            or "line " in resp.text and ".py" in resp.text
        )
        results["no_traceback"] = not traceback_exposed
        print(f"[CHECK] No traceback exposed: {'PASS' if not traceback_exposed else 'FAIL'}")

        # 5. Backend stability
        health_check = requests.get(f"{BASE_URL}/health", timeout=3)
        backend_alive = health_check.status_code == 200 and health_check.json().get("success") is True
        results["backend_stability"] = backend_alive
        print(f"[CHECK] Backend stability (server remains healthy): {'PASS' if backend_alive else 'FAIL'}")

        # Invalid key test overall
        invalid_key_pass = is_controlled_error and friendly_error and not secret_leaked and not traceback_exposed and backend_alive
        results["invalid_key_test"] = invalid_key_pass
        print(f"[CHECK] Overall Invalid-key test: {'PASS' if invalid_key_pass else 'FAIL'}")

    finally:
        stop_backend(backend_proc)

    print("\n==================================================")
    print("STEP 7: Restore Original Configuration Automatically")
    print("==================================================")
    with open(ENV_BACKUP, "r", encoding="utf-8") as f:
        original_content = f.read()
    write_env(original_content)
    
    # Verify restored
    restored_env = read_env()
    restored_key = ""
    for line in restored_env.splitlines():
        if line.startswith("AI_API_KEY="):
            restored_key = line.split("=", 1)[1].strip()
    
    config_restored = (restored_key == "")
    results["config_restored"] = config_restored
    print(f"[CHECK] Configuration restored: {'PASS' if config_restored else 'FAIL'} (AI_API_KEY='{restored_key}')")

    print("\n==================================================")
    print("STEP 8: Restart Backend & Normal AI Analysis")
    print("==================================================")
    normal_backend = start_backend()
    normal_analysis_pass = False
    try:
        norm_resp = requests.post(f"{BASE_URL}/analysis", json=payload, timeout=15)
        print(f"Normal Request HTTP Status: {norm_resp.status_code}")
        if norm_resp.status_code == 200:
            norm_data = norm_resp.json()
            if norm_data.get("success") and "analysis" in norm_data.get("data", {}):
                audit = norm_data["data"]["analysis"]
                required_keys = ["blind_spots", "assumptions", "verification", "potential_conflicts", "missing_factors", "critical_questions"]
                if all(k in audit and len(audit[k]) > 0 for k in required_keys):
                    normal_analysis_pass = True
                    print("[+] All 6 audit categories present in normal analysis result")
                    # Check trace
                    first_bs = audit["blind_spots"][0]
                    if "trace" in first_bs and "trigger" in first_bs["trace"]:
                        print("[+] Traceable reasoning validated")
        results["normal_analysis"] = normal_analysis_pass
        print(f"[CHECK] Normal AI analysis after restoration: {'PASS' if normal_analysis_pass else 'FAIL'}")
    finally:
        # Keep backend running if desired or leave it up
        pass

    print("\n==================================================")
    print("TEST 2 SUMMARY REPORT")
    print("==================================================")
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print(f"Invalid-key test: {'PASS' if results.get('invalid_key_test') else 'FAIL'}")
    print(f"Friendly error: {'PASS' if results.get('friendly_error') else 'FAIL'}")
    print(f"Backend stability: {'PASS' if results.get('backend_stability') else 'FAIL'}")
    print(f"Secret protection: {'PASS' if results.get('secret_protection') else 'FAIL'}")
    print(f"Configuration restored: {'PASS' if results.get('config_restored') else 'FAIL'}")
    print(f"Normal AI analysis after restoration: {'PASS' if results.get('normal_analysis') else 'FAIL'}")

    # Clean up backup
    if os.path.exists(ENV_BACKUP):
        os.remove(ENV_BACKUP)

if __name__ == "__main__":
    run_test()
