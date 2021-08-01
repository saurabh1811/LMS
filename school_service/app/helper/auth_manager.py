from app.helper.auth_bearer import JWTBearer
from fastapi import Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from fastapi import APIRouter, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class LoggedInUser(BaseModel):
	id: int = 0
	userid: str =""
	guid: str=""
	username: str=""
	email: Optional[str] = None
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	schoolId : Optional[str] = None
	mobile : Optional[str] = None



async def get_current_user(token: str = Depends(oauth2_scheme)):
	user_dict = JWTBearer().decodeJWT(token)
	print (user_dict)
	current_user: LoggedInUser= LoggedInUser()
	current_user.id = user_dict['user']['user_id']
	current_user.userid = user_dict['user']['user_id']
	current_user.guid = user_dict['user']['user_guid']
	current_user.username = user_dict['user']['username']
	current_user.email = user_dict['user']['email']
	current_user.first_name = user_dict['user']['first_name']
	current_user.last_name = user_dict['user']['last_name']
	# current_user.schoolId = user_dict['user']['schoolId']
	# current_user.mobile = user_dict['user']['mobile']
	
	return current_user