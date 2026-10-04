from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.schemas.response import APIResponse
from app.services.auth_service import auth_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=APIResponse[TokenResponse])
def register(data: UserRegister, db: Session = Depends(get_db)):
    result = auth_service.register_user(db=db, data=data)
    return APIResponse.ok(data=result, message="User registered successfully")

@router.post("/login", response_model=APIResponse[TokenResponse])
def login(data: UserLogin, db: Session = Depends(get_db)):
    result = auth_service.login_user(db=db, data=data)
    return APIResponse.ok(data=result, message="Login successful")

@router.get("/me", response_model=APIResponse[UserResponse])
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    user_response = UserResponse.model_validate(current_user)
    return APIResponse.ok(data=user_response, message="Current user profile retrieved")
