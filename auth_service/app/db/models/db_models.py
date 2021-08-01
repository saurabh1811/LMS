from app.api.models.shared.shared_models import BaseResponseModel, BaseRequestModel
from typing import List, Optional
import fastapi
from pydantic import BaseModel, validator
from fastapi import HTTPException

class UserDb(BaseModel):
	username: str
	email: str
	mobile: str
	full_name: Optional[str] = None
	disabled: Optional[bool] = None
	schoolId: str

	@validator('email', pre=True)
	def valid_user_existing(cls, v, values, **kwargs):
		if (v is None):
			raise ValueError('Either User not exist or passowrd does not match')
		return v
	

class DbUser(BaseModel):
	username: str
	email: str
	password: str
	confirm_password: str
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	mobile: str
	schoolId: str

	
class UpdateDbUser(BaseModel):
	username: str
	email: str
	user_id:str
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	schoolId: str
	mobile: str



class UserInDB(UserDb):
	hashed_password: str


class DbUserInDB(DbUser):
	hashed_password: str=""
	user_id: str
	guid: str=""


class GoogleUser(BaseResponseModel, BaseModel):
	email: str
	given_name: str
	family_name: str =""
	picture: Optional[str]=""
	at_hash: str =""
	schoolId: Optional[str]="IN"
	

class LoginDbRequestModel(BaseModel):
	username: str
	password: str

class LoginEmailDbRequestModel(BaseModel):
	google_user: GoogleUser

	
class LoginDbResponseModel(BaseModel):
	user: UserInDB

	

class SignupDbRequestModel(BaseModel):
	user: DbUser

class SignupDbResponseModel(BaseModel):
	user: DbUserInDB={}

class UserListDbResponse(BaseModel):
	user_list: List[UserInDB] = []

class UpdateUserDbRequest(BaseModel):
	user: UserInDB
	
class UpdateUserDbResponse(BaseModel):
	user: UserInDB

class ResetPasswordDbRequest(BaseModel):
	password: str =""
	confirm_password: str =""
	user_id: str ="0"

class ResetPasswordDbResponse(BaseModel):
	user: UserInDB={}

class UserDbRequest(BaseRequestModel, BaseModel):
	user_id: int = 0
class UserDbResponse(BaseResponseModel, BaseModel):
	user: DbUserInDB={}

class UpdateUserDbRequest(BaseRequestModel, BaseModel):
	user: UpdateDbUser = {}
class UpdateUserDbResponse(BaseResponseModel, BaseModel):
	user: UserInDB = {}
