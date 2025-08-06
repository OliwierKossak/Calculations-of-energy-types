from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Float
import datetime

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    creation_date = Column(DATETIME,default=datetime.datetime.now())


class Data(Base):
    __tablename__ = "Data"

    data_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    creation_date = Column(DATETIME, default=datetime.datetime.now())
    energy_type = Column(String)
    energy_consumption = Column(Float)

