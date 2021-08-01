from typing import List
from app.services.models import User as s_User, SignupServiceRequest, ResetPasswordServiceRequest
from app.db.models import User as DbUser, SignupDbRequestModel, SignupDbResponseModel, ResetPasswordDbRequest

class ServiceToDbModelConverter:
	def __init__(self):
		self.pro = "Yes!"

	def ToDbModel(self, request: SignupServiceRequest)->SignupDbRequestModel:
		response: SignupDbRequestModel = SignupDbRequestModel
		db_user:DbUser = self.ToDbModelSingle(request.user)
		response.user = db_user
		return response
	def ToDbModelSingle(self, request: s_User)->DbUser:
		resp:DbUser = DbUser(
				username=request.username,
				email=request.email,
				password= request.password,
				first_name = request.first_name,
				last_name=request.last_name,
				schoolId= request.schoolId,
				mobile = request.mobile
		)
		return resp
	
	def ToDbModelReset(self, request: ResetPasswordServiceRequest)-> ResetPasswordDbRequest:
		response: ResetPasswordDbRequest = ResetPasswordDbRequest()
		response.password = request.password
		response.confirm_password = request.confirm_password
		return response

	
	

	
	

