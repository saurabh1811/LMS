from app.services.models.auth_service_model import UserListServiceResponse
from app.db.models import User
from app.services.models import TokenServiceResponse, SignupServiceResponse, SignedUser, User as s_User
from typing import Optional
from app.db.models import (LoginDbResponseModel,LoginDbRequestModel, SignupDbResponseModel, DbUserInDB as DbUser, UserListDbResponse)
from datetime import datetime, timedelta
from app.helper.auth_bearer import JWTBearer




class DbToServiceModelConverter:
	def __init__(self):
		pass

	

	def ToServiceModel(self, request:LoginDbResponseModel)->TokenServiceResponse:
		response:TokenServiceResponse = TokenServiceResponse(access_token="", token_type="bearer")
		user:User=User(username=request.user.email)
		user.email=request.user.email
		token_model = JWTBearer().signJWT(request.user)
		response.access_token = token_model.access_token
		return response

	def ToServiceModelSignup(self, request:SignupDbResponseModel)->SignupServiceResponse:
		response:SignupServiceResponse = SignupServiceResponse(user=SignedUser(username="", hashed_password="", email="", user_id="",mobile="",schoolId=""))
		service_user: SignedUser = self.DbToServiceModel(request.user)
		response.user = service_user
		return response

	

	def DbToServiceModel(self, request:DbUser)->SignedUser:
		resp:SignedUser = SignedUser(
				email=request.email,
				hashed_password=request.password,
				user_id = str(request.guid),
				guid = str(request.guid),
				school_name = request.school_name,
				board=request.board,
				mobile= request.mobile,
				address = request.address
		)
		
		return resp


	def ToServiceModelList(self, request: UserListDbResponse)->UserListServiceResponse:
		response:UserListServiceResponse = UserListServiceResponse()
		for user in request.user_list:
			response.user_list.append(self.DbToServiceModel(user))
		return response

	

