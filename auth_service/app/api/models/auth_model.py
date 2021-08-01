from pydantic import BaseModel, validator
from typing import Optional, List

from sqlalchemy.sql.sqltypes import Boolean
from app.api.models.shared.shared_models import (BaseResponseModel)
import re



class TokenApiResponse(BaseResponseModel,BaseModel):
	access_token: str
	token_type: str
	error: bool = False
	message: str = ""

class User(BaseModel):
	username: str
	email: str
	user_id: str
	guid: str=""
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	mobile: str
	schoolId: str

class SignupApiRequest(BaseModel):
	username: str
	email: str
	password: str
	confirm_password: str
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	mobile: str
	active: bool = True
	schoolId: str

	@validator('email')
	def valid_email(cls, v):
		regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
		if (re.search(regex, v) is None):
			raise ValueError('Provided Email is not valid email')
		return v
	@validator('password')
	def valid_password(cls, v):
		if(v==""):
			raise ValueError('Password cannot be empty!')
		return v
	
	@validator('confirm_password')
	def passwords_match(cls, v, values, **kwargs):
		if (v != values['password']):
			raise ValueError('Password and Confirm Password are not same!')
		return v
	
class UpdateUserRequest(BaseModel):
	username: str
	email: str
	first_name: Optional[str]=""
	last_name: Optional[str]=""
	schoolId: str
	mobile: str
	


	@validator('email')
	def valid_email(cls, v):
		regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
		if (re.search(regex, v) is None):
			raise ValueError('Provided Email is not valid email')
		return v
	
	

	

class SignupApiResponse(BaseResponseModel,BaseModel):
	user: User
	error: bool = False
	message: str = ""

class UserListApiResponse(BaseResponseModel,BaseModel):
	user_list: List[User]

class UpdateUserApiRequest(BaseModel):
	user: UpdateUserRequest

class UpdateUserApiRequestById(BaseModel):
	user: UpdateUserRequest
	userid: str=""

class UpdateUserApiResponse(BaseResponseModel,BaseModel):
	user: User

class ResetPasswordApiRequest(BaseModel):
	password: str =""
	confirm_password: str =""
class ResetPasswordApiResponse(BaseResponseModel,BaseModel):
	user: User

class UserApiResponse(BaseResponseModel,BaseModel):
	user: User