from typing import List, Optional
from pydantic import BaseModel, validator
from app.db.models import UserInDB

class LoginDbRequestModel(BaseModel):
	email: str
	password: str
	
class LoginDbResponseModel(BaseModel):
	user: UserInDB



