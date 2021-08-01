import re
from starlette import responses
from app.services.models.auth_service_model import UpdateUserServiceRequestById
from app.api.models.auth_model import UpdateUserApiRequestById
from app.api.models import (SignupApiRequest, ResetPasswordApiRequest, UpdateUserApiRequest, UpdateUserRequest)
from app.services.models import User as s_User, SignupServiceRequest, ResetPasswordServiceRequest, UserServiceRequest, UpdateUserServiceRequest, UpdateUser
class ApiToServiceModelConverter:
	def __init__(self):
		self.pro = "Yes!"
	
	def ToServiceModel(self, request: SignupApiRequest)->SignupServiceRequest:
		response: SignupServiceRequest = SignupServiceRequest(user=s_User(username="",email="",password="",confirm_password="",mobile="",schoolId=""))
		service_user: s_User = self.ToServiceModelSingle(request)
		response.user = service_user
		return response

	def ToServiceModelSingle(self, request: SignupApiRequest)->s_User:
		resp:s_User = s_User(
				
				email=request.email,
				password= request.password,
				confirm_password = request.confirm_password,
				school_name = request.school_name,
				board=request.board,
				mobile= request.mobile,
				address= request.address
		)
		return resp
	def ToServiceModelReset(self, request: ResetPasswordApiRequest)->ResetPasswordServiceRequest:
		response: ResetPasswordServiceRequest = ResetPasswordServiceRequest()
		response.password = request.password
		response.confirm_password = request.confirm_password
		return response

	def ToServiceModelGetUser(self, id: int)->UserServiceRequest:
		response: UserServiceRequest = UserServiceRequest()
		response.user_id = id
		return response
	
	def ToServiceModelUpdate(self, request: UpdateUserApiRequest)->UpdateUserServiceRequest:
		response: UpdateUserServiceRequest = UpdateUserServiceRequest()
		service_user: UpdateUser = self.ToServiceModelSingleUpdate(request.user)
		response.user = service_user
		return response 
	def ToServiceModelSingleUpdate(self, request: UpdateUserRequest)->UpdateUser:
		resp:UpdateUser = UpdateUser(
				email=request.email,
				school_name = request.school_name,
				board=request.board,
				mobile= request.mobile,
				address= request.address
		)
		return resp

	def ToServiceModelUpdateById(self, request: UpdateUserApiRequestById)-> UpdateUserServiceRequestById:
		response: UpdateUserServiceRequestById = UpdateUserServiceRequestById()
		service_user: UpdateUser = self.ToServiceModelSingleUpdate(request.user)
		response.user = service_user
		response.user_id = request.userid
		return response