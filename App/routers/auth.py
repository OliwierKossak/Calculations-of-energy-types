from fastapi import APIRouter, HTTPException
from ..models import User
from pydantic import BaseModel, Field
from datetime import datetime



class User(BaseModel):
    user_id: int
    email: str
    password: str
    role: str
    creation_date: datetime
