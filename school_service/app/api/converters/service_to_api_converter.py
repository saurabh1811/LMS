from app.api.models import (TokenApiResponse, SignupApiResponse, User as api_User, UserListApiResponse)
from app.services.models import (TokenServiceResponse, SignupServiceResponse, User as s_User, UserListServiceResponse)



class ServiceToApiModelConverter:
	def __init__(self):
		pass
	
	def ToAPIModel(self,request: TokenServiceResponse)->TokenApiResponse:
		response:TokenApiResponse = TokenApiResponse(access_token="",token_type="")
		response.access_token= request.access_token
		response.token_type= request.token_type
		response.error = False
		response.message=""
		return response
	
	def ToAPIModelSingup(self,request: SignupServiceResponse)->SignupApiResponse:
		response:SignupApiResponse = SignupApiResponse(user=api_User(email="",mobile="", hashed_password="", board="",school_name="",address=""))
		api_resp_user: api_User = self.ToApiModelUser(request.user)
		response.user = api_resp_user
		response.error = False
		response.message=""
		return response

	def ToApiModelUser(self, request: s_User)->api_User:
		resp:api_User = api_User(
				email=request.email,
				school_name = request.school_name,
				board=request.board,
				mobile= request.mobile,
				address= request.address,
				
		)
		return resp

	def ToAPIModelUserList(self, request: UserListServiceResponse)->UserListApiResponse:
		response:UserListApiResponse = UserListApiResponse(user_list=[])
		for user in request.user_list:
			response.user_list.append(self.ToApiModelUser(user))
		return response

