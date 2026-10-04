import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

def run_e2e_tests():
    print("========================================")
    print("STARTING COMPLETE END-TO-END SUITE")
    print("========================================")

    # 1. Health Check
    print("\n1. Testing GET /health...")
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    health_data = r.json()
    assert health_data["success"] is True
    print("   [PASS] Health check is healthy and returns standard envelope.")

    # 2. Authentication: Register
    unique_email = f"user_{uuid.uuid4().hex[:6]}@blindspot.ai"
    print(f"\n2. Testing POST /auth/register with {unique_email}...")
    reg_payload = {
        "name": "Alex Developer",
        "email": unique_email,
        "password": "Password123!"
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    assert r.status_code == 200, f"Registration failed: {r.text}"
    token_data = r.json()["data"]
    token = token_data["access_token"]
    user_id = token_data["user"]["id"]
    print("   [PASS] User registered successfully and received JWT token.")

    # 3. Auth: Duplicate Email Rejection
    print("\n3. Testing duplicate email registration...")
    r = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    assert r.status_code == 400, f"Duplicate check failed: {r.text}"
    print("   [PASS] Duplicate registration rejected with HTTP 400.")

    # 4. Auth: Wrong Password Login
    print("\n4. Testing wrong password login...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": unique_email, "password": "WrongPassword"})
    assert r.status_code == 401, f"Wrong password check failed: {r.text}"
    print("   [PASS] Wrong password rejected with HTTP 401.")

    # 5. Auth: Valid Login
    print("\n5. Testing valid login...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": unique_email, "password": "Password123!"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    login_token = r.json()["data"]["access_token"]
    print("   [PASS] Login successful and returned active JWT.")

    # 6. Auth: Protected Route /auth/me
    print("\n6. Testing protected GET /auth/me...")
    # Without token
    r_unauth = requests.get(f"{BASE_URL}/auth/me")
    assert r_unauth.status_code == 401, f"Expected 401 unauth: {r_unauth.text}"
    # With token
    headers = {"Authorization": f"Bearer {token}"}
    r_auth = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert r_auth.status_code == 200, f"Protected route failed: {r_auth.text}"
    assert r_auth.json()["data"]["email"] == unique_email
    print("   [PASS] Protected endpoint correctly blocks unauthenticated requests and admits valid token.")

    # 7. Decision Input & AI Reasoning Engine: Scenario 1 (Internship Dilemma)
    print("\n7. Testing POST /analysis (Scenario 1: Internship Dilemma)...")
    internship_req = {
        "decision": "Accept a 6-month startup internship instead of completing university semester",
        "context": "Senior CS student with 2 semesters remaining. The startup has 4 engineers. Stipend is $3,500/mo.",
        "reasoning": "The stipend is good and startup experience will guarantee higher-paying job offers later."
    }
    r = requests.post(f"{BASE_URL}/analysis", json=internship_req, headers=headers)
    assert r.status_code == 200, f"Analysis failed: {r.text}"
    analysis_data = r.json()["data"]
    audit = analysis_data["analysis"]
    decision_1_id = analysis_data["decision_id"]

    # Verify all 6 mandatory categories
    assert len(audit["blind_spots"]) > 0, "Missing blind spots"
    assert len(audit["assumptions"]) > 0, "Missing assumptions"
    assert len(audit["verification"]) > 0, "Missing verification"
    assert len(audit["potential_conflicts"]) > 0, "Missing potential conflicts"
    assert len(audit["missing_factors"]) > 0, "Missing missing factors"
    assert len(audit["critical_questions"]) > 0, "Missing critical questions"
    print("   [PASS] 6 audit categories returned and populated.")
    print("   - Blind Spot Sample:", audit["blind_spots"][0]["finding"][:70], "...")
    print("   - Assumption Sample:", audit["assumptions"][0]["assumption"][:70], "...")
    print("   - Verification Sample:", audit["verification"][0]["verification"][:70], "...")
    print("   - Conflict Sample:", audit["potential_conflicts"][0]["conflict"][:70], "...")

    # 8. Scenario 2: Laptop Purchase
    print("\n8. Testing POST /analysis (Scenario 2: Hardware Purchase)...")
    laptop_req = {
        "decision": "Buy a $2,800 laptop on installment credit",
        "context": "Freelance designer with working laptop, $4k savings",
        "reasoning": "Higher specs will make me work faster and pay for itself."
    }
    r = requests.post(f"{BASE_URL}/analysis", json=laptop_req, headers=headers)
    assert r.status_code == 200, f"Laptop analysis failed: {r.text}"
    laptop_audit = r.json()["data"]["analysis"]
    assert any("durability" in b["finding"].lower() or "cost" in b["finding"].lower() or "price" in b["finding"].lower() for b in laptop_audit["blind_spots"])
    print("   [PASS] Hardware purchase scenario dynamically produced hardware-relevant factors.")

    # 9. Scenario 3: Validation & Error Handling
    print("\n9. Testing input validation on short/empty input...")
    invalid_req = {
        "decision": "No",
        "context": "",
        "reasoning": "ok"
    }
    r = requests.post(f"{BASE_URL}/analysis", json=invalid_req, headers=headers)
    assert r.status_code == 422, f"Expected 422 for short input: {r.text}"
    print("   [PASS] Short/empty input correctly rejected with HTTP 422 and validation error.")

    # 10. Database & History: GET /decisions
    print("\n10. Testing GET /decisions (History)...")
    r = requests.get(f"{BASE_URL}/decisions", headers=headers)
    assert r.status_code == 200, f"History fetch failed: {r.text}"
    history_list = r.json()["data"]
    assert len(history_list) >= 2, f"Expected at least 2 decisions, got {len(history_list)}"
    print(f"   [PASS] Successfully retrieved {len(history_list)} historical decision records.")

    # 11. GET /decisions/{id} Single Item Retrieval
    print(f"\n11. Testing GET /decisions/{decision_1_id}...")
    r = requests.get(f"{BASE_URL}/decisions/{decision_1_id}", headers=headers)
    assert r.status_code == 200, f"Single decision retrieval failed: {r.text}"
    single_data = r.json()["data"]
    assert single_data["decision"] == internship_req["decision"]
    assert single_data["analysis"] is not None
    print("   [PASS] Single decision audit retrieved with full analysis JSON.")

    # 12. Security Check: Cross-User Authorization Barrier
    print("\n12. Testing Cross-User Access Barrier...")
    other_user_email = f"other_{uuid.uuid4().hex[:6]}@blindspot.ai"
    r_other = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Other User",
        "email": other_user_email,
        "password": "Password123!"
    })
    other_token = r_other.json()["data"]["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Other user tries to access User A's decision
    r_forbidden = requests.get(f"{BASE_URL}/decisions/{decision_1_id}", headers=other_headers)
    assert r_forbidden.status_code == 403, f"Expected 403 Forbidden, got {r_forbidden.status_code}"
    print("   [PASS] Cross-user access strictly blocked with HTTP 403 Forbidden.")

    # 13. Dashboard Metrics: GET /dashboard
    print("\n13. Testing GET /dashboard...")
    r = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    assert r.status_code == 200, f"Dashboard metrics failed: {r.text}"
    dash_data = r.json()["data"]
    assert dash_data["total_decisions"] >= 2
    assert len(dash_data["recent_decisions"]) >= 2
    print(f"   [PASS] Dashboard metrics: Total={dash_data['total_decisions']}, Recent={len(dash_data['recent_decisions'])}")

    print("\n========================================")
    print("ALL END-TO-END HTTP INTEGRATION TESTS PASSED!")
    print("========================================")

if __name__ == "__main__":
    run_e2e_tests()
