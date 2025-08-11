from fastapi import APIRouter, HTTPException, Depends
from ..models import User
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime
from starlette import status
from ..database import get_db

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]


class UserRequestModel(BaseModel):
    user_id: int
    email: str
    password: str
    role: str
    creation_date: datetime


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequestModel):
    create_user_model = User(
        user_id=user_request.user_id,
        email=user_request.email,
        password=user_request.password,
        role=user_request.role,
        creation_date=user_request.creation_date
    )
    db.add(create_user_model)
    db.commit()

