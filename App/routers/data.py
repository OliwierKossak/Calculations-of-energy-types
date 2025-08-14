from fastapi import APIRouter, HTTPException, Depends, UploadFile
from datetime import timedelta, timezone
from ..models import User
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from starlette import status
from ..database import get_db
from .auth import get_current_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter(
    prefix='/data',
    tags=['data']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@router.post("/upload_data", status_code=status.HTTP_201_CREATED)
async def save_excel_data_to_db(file: UploadFile,user: user_dependency, db: db_dependency):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail='Format of file need to be .xlsx or .xls')




