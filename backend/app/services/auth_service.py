from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

class AuthService:
    @staticmethod
    def register_user(db: Session, data: UserRegister) -> TokenResponse:
        # Check if email is already taken
        existing_user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )

        new_user = User(
            name=data.name.strip(),
            email=data.email.lower().strip(),
            password_hash=hash_password(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Issue access token
        access_token = create_access_token(
            data={"sub": new_user.id, "email": new_user.email}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(new_user)
        )

    @staticmethod
    def login_user(db: Session, data: UserLogin) -> TokenResponse:
        user = db.query(User).filter(User.email == data.email.lower().strip()).first()
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            data={"sub": user.id, "email": user.email}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

auth_service = AuthService()
