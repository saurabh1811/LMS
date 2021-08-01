from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt
from datetime import datetime
import time

from typing import Optional
from datetime import datetime, timedelta
from typing import Dict
from pydantic import BaseModel
from app.core.settings import JWTConfig
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
	username: str
	email: Optional[str] = None
	full_name: Optional[str] = None
	disabled: Optional[bool] = None
	
	
class UserInDB(User):
	hashed_password: str
	id: int =  0
	guid: str =""
	schoolId : str = ""
	mobile : str 
	first_name : str
	last_name : str


class Token(BaseModel):
	access_token: str



class JWTBearer(HTTPBearer):
	def __init__(self, auto_error: bool = True):
		self.secret_key = JWTConfig().secret_key
		self.algorithm =  JWTConfig().algorithm
		self.access_token_expire_minutes =  JWTConfig().access_token_expire_minutes

		super(JWTBearer, self).__init__(auto_error=auto_error)

	def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=15)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
		return encoded_jwt
	


	def signJWT(self, user: UserInDB) -> Token:
		payload = {
			"user": {"user_guid": str(user.guid), "user_id": user.id, "username": user.username, "first_name": user.first_name, "last_name": user.last_name, "email": user.email, "schoolId": user.schoolId,"mobile":user.mobile },
			"expires": time.time() + self.access_token_expire_minutes
		}
		token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
		return Token(access_token=token)


	async def __call__(self, request: Request):
		credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
		if credentials:
			if not credentials.scheme == "Bearer":
				raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
			if not self.verify_jwt(credentials.credentials):
				raise HTTPException(status_code=403, detail="Invalid token or expired token.")
			return credentials.credentials
		else:
			raise HTTPException(status_code=403, detail="Invalid authorization code.")

	def decodeJWT(self, token: str) -> dict:
		try:
			decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
			return decoded_token if decoded_token["expires"] >= time.time() else None
		except:
			return {}

	def verify_jwt(self, jwtoken: str) -> bool:
		isTokenValid: bool = False

		try:
			payload = self.decodeJWT(jwtoken)
		except:
			payload = None
		if payload:
			isTokenValid = True
		return isTokenValid

	
