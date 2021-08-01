from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, validator
from app.db import Base
from fastapi_restful.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
	__tablename__ = "students"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
	username = Column(String, unique=True, index=True)
	email= Column(String, unique=True, index=True)
	password= Column(String,  nullable=True)
	first_name= Column(String,  nullable=True)
	last_name=Column(String,   nullable=True)
	mobile= Column(String,  nullable=False)
	schoolId = Column(String, nullable=False)
	active = Column(Boolean(), default=True)
