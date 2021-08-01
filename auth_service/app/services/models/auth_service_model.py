
from typing import List,Optional
from pydantic import BaseModel
from sqlalchemy.orm.session import Session
from app.services.models.shared import (BaseServiceRequestModel,BaseServiceResponseModel)
from pydantic import BaseModel, validator
from app.api.models.shared.shared_models import (BaseRequestModel, BaseResponseModel)

class User(BaseResponseModel, BaseModel):
	username: str
	email: str
	password: str
	confirm_password: str
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	mobile: str
	schoolId: str

class UpdateUser(BaseResponseModel, BaseModel):
	username: str
	email: str
	mobile: str
	guid: str =""
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	schoolId: str
	mobile: str

class SignedUser(BaseResponseModel, BaseModel):
	username: str
	email: str
	user_id: str
	guid: str =""
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	mobile: str
	schoolId: str

class GoogleUser(BaseResponseModel, BaseModel):
	email: str
	given_name: str
	family_name: str =""
	picture: Optional[str]=""
	at_hash: str =""
	mobile: str
	schoolId: str

class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	username: Optional[str] = None
	scopes: List[str] = []

class TokenEmailServiceRequest(BaseServiceRequestModel,BaseModel):
	google_user: GoogleUser
	scopes: List[str] = []




class TokenServiceRequest(BaseServiceRequestModel,BaseModel):
	username: str 
	password: str
	
	scopes: List[str] = []

	@validator('username')
	def is_alphanumeric(cls, v):
		if not v.isalnum():
			raise ValueError('username should be alphanumeric')
		return v

class TokenServiceResponse(BaseServiceResponseModel,BaseModel):
	access_token: str
	token_type: str

class SignupServiceRequest(BaseServiceRequestModel,BaseModel):
	user: User
	

	

class SignupServiceResponse(BaseServiceResponseModel,BaseModel):
	user: SignedUser

class UserListServiceResponse(BaseServiceResponseModel,BaseModel):
	user_list: List[SignedUser]=[]

class UpdateUserServiceRequest(BaseModel):
	user: UpdateUser={}
	
class UpdateUserServiceResponse(BaseResponseModel,BaseModel):
	user: SignedUser

class UpdateUserServiceRequestById(BaseRequestModel, BaseModel):
	user: UpdateUser = {}
	user_id: str =""

class ResetPasswordServiceRequest(BaseResponseModel,BaseModel):
	password: str =""
	confirm_password: str =""
	token: str =""
class ResetPasswordServiceResponse(BaseResponseModel,BaseModel):
	user: SignedUser

class UserServiceRequest(BaseRequestModel, BaseModel):
	user_id: int = 0
class UserServiceResponse(BaseResponseModel, BaseModel):
	user: SignedUser

class SelfUserServiceRequest(BaseResponseModel, BaseModel):
	token: str=""