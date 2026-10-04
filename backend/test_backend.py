import sys
sys.path.insert(0, ".")

import asyncio
from app.database.session import init_db, SessionLocal
from app.schemas.auth import UserRegister, UserLogin
from app.services.auth_service import auth_service
from app.schemas.analysis import AnalysisRequest
from app.services.analysis_service import analysis_service
from app.services.decision_service import decision_service
from app.services.dashboard_service import dashboard_service

def test_full_backend():
    print("1. Initializing DB...")
    init_db()
    db = SessionLocal()
    print("   DB initialized.")

    print("2. Testing Registration...")
    reg_data = UserRegister(name="Test User", email="test@blindspot.ai", password="password123")
    try:
        token_resp = auth_service.register_user(db, reg_data)
        print("   Registered user:", token_resp.user.email)
    except Exception as e:
        print("   User might already exist, attempting login...")
        login_data = UserLogin(email="test@blindspot.ai", password="password123")
        token_resp = auth_service.login_user(db, login_data)
        print("   Logged in:", token_resp.user.email)

    user = token_resp.user

    print("3. Testing Analysis...")
    req = AnalysisRequest(
        decision="Accept 6-month startup internship instead of finishing semester",
        context="Senior CS student with 2 semesters remaining; startup has 4 engineers",
        reasoning="The stipend is high and startup experience will improve my career."
    )
    result = asyncio.run(analysis_service.process_analysis(
        request_data=req,
        current_user=user,
        db=db
    ))
    print("   Analysis produced keys:", list(result["analysis"].keys()))
    print("   Blind spots count:", len(result["analysis"]["blind_spots"]))
    print("   Assumptions count:", len(result["analysis"]["assumptions"]))
    print("   Verification count:", len(result["analysis"]["verification"]))
    print("   Conflicts count:", len(result["analysis"]["potential_conflicts"]))
    print("   Missing factors count:", len(result["analysis"]["missing_factors"]))
    print("   Critical questions count:", len(result["analysis"]["critical_questions"]))

    print("4. Testing Decision & Dashboard Services...")
    decisions = decision_service.get_user_decisions(db, user.id)
    print("   User decisions count:", len(decisions))
    if decisions:
        single = decision_service.get_decision_by_id(db, decisions[0].id, user.id)
        print("   Retrieved single decision:", single.decision[:40])
    
    dash = dashboard_service.get_dashboard_data(db, user.id)
    print("   Dashboard total decisions:", dash.total_decisions)

    db.close()
    print("ALL BACKEND INTEGRATION TESTS PASSED!")

if __name__ == "__main__":
    test_full_backend()
