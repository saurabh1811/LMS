
from typing import List,Optional
from pydantic import BaseModel
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import BigInteger
from app.services.models.shared import (BaseServiceRequestModel,BaseServiceResponseModel)
from pydantic import BaseModel, validator
from app.api.models.shared.shared_models import (BaseRequestModel, BaseResponseModel)

class User(BaseResponseModel, BaseModel):
	email: str
	password: str
	confirm_password: str
	school_name: str=""
	address: str=""
	board: Optional[str]=""
	mobile: str

class UpdateUser(BaseResponseModel, BaseModel):
	email: str
	password: str
	guid: str =""
	confirm_password: str
	school_name: str=""
	address: str=""
	board: Optional[str]=""
	mobile: str

class SignedUser(BaseResponseModel, BaseModel):
	email: str
	guid: str =""
	school_name: str=""
	address: str=""
	board: Optional[str]=""
	mobile: str



class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	email: Optional[str] = None
	scopes: List[str] = []






class TokenServiceRequest(BaseServiceRequestModel,BaseModel):
	email: str 
	password: str
	
	scopes: List[str] = []

	

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