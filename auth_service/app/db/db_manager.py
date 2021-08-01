import uuid
from app.services.models.auth_service_model import UserServiceRequest
from pydantic import BaseModel
from app.db.models import (UserInDB, User)
from typing import Generator
from passlib.context import CryptContext
from app.db.models import (DbUserInDB, LoginDbResponseModel,LoginDbRequestModel, 
							SignupDbRequestModel, SignupDbResponseModel
							,UserListDbResponse, ResetPasswordDbRequest, LoginEmailDbRequestModel,
							ResetPasswordDbResponse, UserDbResponse,UpdateUserDbRequest, UpdateUserDbResponse)
from sqlalchemy.orm import Session
from fastapi import Depends


import app.db as models

from app.db.db_base import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)


class dbManager:
	# default constructor
	def __init__(self):
		self.resp = [
		 {
			"username": "johndoe",
			"full_name": "John Doe",
			"email": "johndoe@example.com",
			"hashed_password": "$2b$12$3FfqxrWClRKEAeN8r9RZ2.J0NQWGhGf7oikaQ2Xzhd.lp.n1Av/tK",
			"disabled": False,
			},
    	{
			"username": "alice",
			"full_name": "Alice Chains",
			"email": "alicechains@example.com",
			"hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
			"disabled": True,
		}
		]

		self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
		
	def get_db(self) -> Generator:
		try:
			db = SessionLocal()
			yield db
		finally:
			db.close()



	def __get_password_hash(self, password: str):
		return self.pwd_context.hash(password)

	def __verify_password(self, plain_password, hashed_password):
		return self.pwd_context.verify(plain_password, hashed_password)

		
	def get_user(self, db: Session, request: LoginDbRequestModel)->LoginDbResponseModel:
		user_db=db.query(User).filter(User.username == request.username).first()
		response: LoginDbResponseModel = LoginDbResponseModel(user=UserInDB(username="", hashed_password="",  email="",mobile="",schoolId="" ))
		if user_db is not None:
			if self.__verify_password(request.password, user_db.password):
				response.user = user_db
				print (response.user)
			else:
				response.user = UserInDB(username="", hashed_password="",  email=None )
		else:
			response.user = UserInDB(username="", hashed_password="",  email=None )
		return response
	
	def get_email_user(self, db: Session, request: LoginEmailDbRequestModel)->LoginDbResponseModel:
		user_db=db.query(User).filter(User.username == request.google_user.email).first()
		response: LoginDbResponseModel = LoginDbResponseModel(user=UserInDB(username="", hashed_password="",  email="" ))
		if user_db is not None:
			response.user = user_db
		else:
			db_obj: User = User(username=request.google_user.email, email=request.google_user.email, first_name=request.google_user.given_name, last_name=request.google_user.family_name)
			db_obj.password = request.google_user.at_hash
			db.add(db_obj)
			db.commit()
			response.user = db_obj
		return response

	def add_user(self, db: Session, request: SignupDbRequestModel)->SignupDbResponseModel:
		response: SignupDbResponseModel = SignupDbResponseModel(user=DbUserInDB(username="", hashed_password="", email="", user_id="", password="", confirm_password="",mobile="",schoolId=""))
		hashed_password = self.__get_password_hash(request.user.password)
		db_obj: User = request.user
		db_obj.password = hashed_password
		db.add(db_obj)
		db.commit()
		response.user= DbUserInDB(username=request.user.username, hashed_password=hashed_password, email= request.user.email, user_id= db_obj.id, first_name= db_obj.first_name, last_name= db_obj.last_name, guid= str(db_obj.guid), password=request.user.password, confirm_password=request.user.password,mobile=request.user.mobile,schoolId=request.user.schoolId)
		return response 
		
	
	def get_db_user(self, username:str)-> UserInDB:
		user=self.__fake_db(username)
		if not user:
			return False
		else:
			return user
	
	def get_user_list(self, db: Session)->UserListDbResponse:
		user_db=db.query(User).all()
		response: UserListDbResponse = UserListDbResponse()
		response.user_list = user_db
		return response


	def ResetPassword(self, db: Session, request: ResetPasswordDbRequest)->ResetPasswordDbResponse:
		response: ResetPasswordDbResponse = ResetPasswordDbResponse()
		hashed_password = self.__get_password_hash(request.password)
		user_db=db.query(User).filter(User.id == request.user_id).first()
		user_db.password = hashed_password
		db.commit()
		db.refresh(user_db)
		response.user= DbUserInDB(username=user_db.username, hashed_password=hashed_password, email= user_db.email, user_id= user_db.id, password=hashed_password, confirm_password=request.password,mobile= user_db.mobile,schoolId= user_db.schoolId)
		return response 

	def get_user_detail(self, db: Session, request: UserServiceRequest)->SignupDbResponseModel:
		user_db=db.query(User).filter(User.guid == uuid.UUID(request.user_id)).first()
		response: SignupDbResponseModel = SignupDbResponseModel()
		response.user = user_db
		return response

	def update_user_details(self, db: Session, request: UpdateUserDbRequest)->UpdateUserDbResponse:
		response: UpdateUserDbResponse = UpdateUserDbResponse()
		user_db=db.query(User).filter(User.id == request.userid).first()
		if user_db is not None:
			user_db.username = request.user.username
			user_db.email = request.user.email
			user_db.mobile = request.user.mobile
			user_db.first_name = request.user.first_name
			user_db.last_name = request.user.last_name
			user_db.schoolId = request.user.schoolId
			db.commit()
			db.refresh(user_db)
			response.user = user_db
		
		
		return response

	
		