from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.rate_limit import (
    check_login_rate_limit,
    register_failed_login,
    reset_attempts,
)
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
def login(
    data: RegisterIn,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Логин по email+password, возвращает JWT.
    Для защиты от брутфорса:
    - неуспешные попытки лимитируем (rate limit + счётчик);
    - успешный логин всегда разрешаем и сбрасываем счётчик.
    """
    user = db.query(User).filter(User.email == data.email).first()

    # Если логин/пароль неверные — применяем rate limiting
    if not user or not verify_password(data.password, user.password_hash):
        ip = check_login_rate_limit(request)
        register_failed_login(ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Успешный логин: сбрасываем счётчик для этого IP (если он есть)
    if request.client:
        reset_attempts(request.client.host)

    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)
