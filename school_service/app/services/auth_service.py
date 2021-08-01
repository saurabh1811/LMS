from app.helper.auth_manager import LoggedInUser
from app.services.models.auth_service_model import ResetPasswordServiceRequest, ResetPasswordServiceResponse, UpdateUserServiceRequestById
from app.services.models import (TokenServiceRequest,TokenServiceResponse, 
								SignupServiceRequest, SignupServiceResponse, 
								SignedUser, UserListServiceResponse,
								UserServiceRequest, UserServiceResponse, 
								 SelfUserServiceRequest, UpdateUserServiceRequest, UpdateUserServiceResponse)
from app.services.converters import DbToServiceModelConverter as DbConverter, ServiceToDbModelConverter
from app.db.db_manager import dbManager 
from fastapi import  HTTPException
from app.db.models import (LoginDbResponseModel,LoginDbRequestModel, SignupDbRequestModel
							, User, SignupDbRequestModel, ResetPasswordDbRequest, 
							UserDbRequest, UpdateUserDbRequest)
from sqlalchemy.orm import Session
from app.helper.auth_bearer import JWTBearer




class TokenService:
	def __init__(self):
		self.test = "Test"

	def Login(self, db: Session, request: TokenServiceRequest)->TokenServiceResponse:
		LoginDbRequest:LoginDbRequestModel=LoginDbRequestModel(username=request.username,password=request.password)
		db_response = dbManager().get_user(db, LoginDbRequest)
		print (db_response)
		service_response= DbConverter().ToServiceModel(db_response)      
		return service_response
	

	def Signup(self, db:Session, request: SignupServiceRequest)->SignupServiceResponse:
		print (SignupServiceRequest)
		service_response:SignupServiceResponse=SignupServiceResponse(user=SignedUser(email="",user_id="",hashed_password="",mobile="",school_name="",board="",address=""))
		signup_db_request: SignupDbRequestModel = ServiceToDbModelConverter().ToDbModel(request)
		db_response = dbManager().add_user(db, signup_db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response

	def GetUserList(self, db: Session)->UserListServiceResponse:
		db_response = dbManager().get_user_list(db)
		service_response= DbConverter().ToServiceModelList(db_response)      
		return service_response
	
	def ResetPassword(self, db:Session, request: ResetPasswordServiceRequest)-> ResetPasswordServiceResponse:
		service_response: ResetPasswordServiceResponse=ResetPasswordServiceResponse(user=SignedUser(username="",email="",user_id="",hashed_password="",mobile="",schoolId=""))
		db_request: ResetPasswordDbRequest = ServiceToDbModelConverter().ToDbModelReset(request)
		user_dict = JWTBearer().decodeJWT(request.token)
		db_request.user_id= str(user_dict['user']['user_id'])
		db_response = dbManager().ResetPassword(db, db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response
	
	def GetUser(self, db: Session, request: UserServiceRequest)->UserServiceResponse:
		db_request: UserDbRequest = UserDbRequest()
		db_request.user_id = request.user_id
		db_response = dbManager().get_user_detail(db, db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response

	def GetSelfUser(self, db: Session, current_user: LoggedInUser)-> UserServiceResponse:
		db_request: UserDbRequest = UserDbRequest()
		db_request.user_id= current_user.guid
		print (current_user.userid)
		db_response = dbManager().get_user_detail(db, db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response

	def UserUpdate(self, db: Session, request: UpdateUserServiceRequest, current_user: LoggedInUser)-> UpdateUserServiceResponse:
		db_request: UpdateUserDbRequest = UpdateUserDbRequest()
		db_request.userid= current_user.userid
		db_request.user = request.user
		db_response = dbManager().update_user_details(db, db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response
	
	def UserUpdateById(self, db: Session, request: UpdateUserServiceRequestById, current_user: LoggedInUser)-> UpdateUserServiceResponse:
		db_request: UpdateUserDbRequest = UpdateUserDbRequest()
		db_request.userid= request.user_id
		db_request.user = request.user
		db_response = dbManager().update_user_details(db, db_request)
		service_response= DbConverter().ToServiceModelSignup(db_response)      
		return service_response

	def RefreshToken(self, db: Session, current_user: LoggedInUser)->LoginDbResponseModel:
		response: TokenServiceResponse = TokenServiceResponse(access_token="", token_type="bearer")
		token_model = JWTBearer().signJWT(current_user)
		response.access_token = token_model.access_token
		return response

		

		

	

