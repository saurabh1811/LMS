from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, validator
from app.db import Base
from fastapi_restful.guid_type import GUID, GUID_DEFAULT_SQLITE


class User(Base):
	__tablename__ = "school"

	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
	email= Column(String, unique=True, index=True)
	password= Column(String,  nullable=True)
	school_name= Column(String,  nullable=True)
	board=Column(String,   nullable=True)
	mobile= Column(String,  nullable=False)
	address = Column(String, nullable=False)
	
