from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user, get_db
from app.models.user import User
from app.models.wish import Wish
from app.schemas.wish import WishCreate, WishOut, WishUpdate

router = APIRouter(prefix="/wishes", tags=["wishes"])


def ensure_owner(w: Wish, user: User):
    if w.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail={"error": {"code": "forbidden", "message": "Forbidden"}},
        )


@router.get("/", response_model=List[WishOut])
def list_wishes(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    price_lt: Optional[float] = Query(None, alias="price<", ge=0),
):
    q = db.query(Wish).filter(Wish.owner_id == user.id)
    if price_lt is not None:
        q = q.filter(Wish.price_estimate is not None).filter(
            Wish.price_estimate < price_lt
        )
    return q.order_by(Wish.id.desc()).all()


@router.post("/", response_model=WishOut, status_code=201)
def create_wish(
    payload: WishCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    w = Wish(
        title=payload.title,
        link=str(payload.link) if payload.link else None,
        price_estimate=payload.price_estimate,
        notes=payload.notes,
        owner_id=user.id,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@router.get("/{wish_id}", response_model=WishOut)
def get_wish(
    wish_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    w = db.get(Wish, wish_id)
    if not w:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Not found"}},
        )
    ensure_owner(w, user)
    return w


@router.put("/{wish_id}", response_model=WishOut)
def update_wish(
    wish_id: int,
    payload: WishUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    w = db.get(Wish, wish_id)
    if not w:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Not found"}},
        )
    ensure_owner(w, user)

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "link" and value is not None:
            setattr(w, field, str(value))
        else:
            setattr(w, field, value)

    db.commit()
    db.refresh(w)
    return w


@router.delete("/{wish_id}", status_code=204)
def delete_wish(
    wish_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    w = db.get(Wish, wish_id)
    if not w:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "not_found", "message": "Not found"}},
        )
    ensure_owner(w, user)
    db.delete(w)
    db.commit()
    return None
