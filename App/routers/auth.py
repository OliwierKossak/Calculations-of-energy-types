from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta, timezone
from ..models import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from starlette import status
from ..database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

SECRET_KEY = 'bda4eea505e79437178ef7363b92563ca4a9d1d9d737d2c218b24e3b69b8cf6c'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]


class UserRequestModel(BaseModel):
    user_id: Optional[int] = None
    email: str
    password: str
    role: str
    creation_date: datetime


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequestModel):
    create_user_model = User(
        user_id=user_request.user_id,
        email=user_request.email,
        password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        creation_date=user_request.creation_date
    )

    db.add(create_user_model)
    db.commit()

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    print("form_data.username: ",form_data.username)
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return HTTPException(status_code=404, detail='Failed Authentication')
    token = create_access_token(user.email, user.user_id, timedelta(minutes=20))

    return token

