from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_db,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import RegisterIn, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        user = User(email=data.email, password_hash=hash_password(data.password))
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)


@router.post("/login", response_model=TokenOut)
def login(data: RegisterIn, db: Session = Depends(get_db)):
    """
    Логин по email+password, возвращает JWT.
    """
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)
