from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Secret

from ..schemas import (
    SecretCreate,
    SecretUpdate
)

from ..dependencies import get_current_user

router = APIRouter(
    prefix="/secrets",
    tags=["Secrets"]
)

@router.post("")
def create_secret(
    data: SecretCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    secret = Secret(
        title=data.title,
        content=data.content,
        owner_id=current_user.id
    )

    db.add(secret)
    db.commit()
    db.refresh(secret)

    return secret

@router.get("")
def get_my_secrets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Secret).filter(
        Secret.owner_id == current_user.id
    ).all()

@router.get("/{secret_id}")
def get_secret(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    secret = db.query(Secret).filter(
        Secret.id == secret_id,
        Secret.owner_id == current_user.id
    ).first()

    if not secret:
        raise HTTPException(
            status_code=404,
            detail="Secret not found"
        )

    return secret

@router.patch("/{secret_id}")
def update_secret(
    secret_id: int,
    data: SecretUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    secret = db.query(Secret).filter(
        Secret.id == secret_id,
        Secret.owner_id == current_user.id
    ).first()

    if not secret:
        raise HTTPException(
            status_code=404,
            detail="Secret not found"
        )

    if data.title is not None:
        secret.title = data.title

    if data.content is not None:
        secret.content = data.content

    db.commit()

    return secret

@router.delete("/{secret_id}")
def delete_secret(
    secret_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    secret = db.query(Secret).filter(
        Secret.id == secret_id,
        Secret.owner_id == current_user.id
    ).first()

    if not secret:
        raise HTTPException(
            status_code=404,
            detail="Secret not found"
        )

    db.delete(secret)
    db.commit()

    return {"message": "Deleted"}

from sqlalchemy import or_


@router.get("/search/")
def search_secret(
    text: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Secret).filter(
        Secret.owner_id == current_user.id,
        or_(
            Secret.title.ilike(f"%{text}%"),
            Secret.content.ilike(f"%{text}%")
        )
    ).all()