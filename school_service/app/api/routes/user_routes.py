from app.api.models.auth_model import UpdateUserApiRequestById
from fastapi import  APIRouter,Depends
from fastapi.security import (OAuth2PasswordRequestForm)
from app.api.models import ( TokenApiResponse, SignupApiResponse, 
                            SignupApiRequest, UserListApiResponse
                            , UpdateUserApiResponse, UpdateUserApiRequest
                            , UserApiResponse)
from app.api.converters import ServiceToApiModelConverter, ApiToServiceModelConverter
from app.services.auth_service import (TokenService, SignupServiceRequest, SignupServiceResponse)
from app.services.models import (TokenServiceResponse,TokenServiceRequest,
                                 UserListServiceResponse, UpdateUserServiceRequest, 
                                 UpdateUserServiceResponse, UserServiceRequest, 
                                 UserServiceResponse, UpdateUserServiceRequestById)
from sqlalchemy.orm import Session
from app.api import deps
from app.helper import LoggedInUser, get_current_user
from app.helper.auth_bearer import JWTBearer, oauth2_scheme



user = APIRouter()

@user.put('/', response_model=UpdateUserApiResponse, response_model_exclude_unset=True, dependencies=[Depends(JWTBearer())])
async def update_user(request: UpdateUserApiRequest, db: Session = Depends(deps.get_db), current_user: LoggedInUser = Depends(get_current_user))->UpdateUserApiResponse :
    service_request:UpdateUserServiceRequest =ApiToServiceModelConverter().ToServiceModelUpdate(request)
    service_response:UpdateUserServiceResponse =  TokenService().UserUpdate(db, service_request, current_user)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model

@user.put('/{id}', response_model=UpdateUserApiResponse, response_model_exclude_unset=True, dependencies=[Depends(JWTBearer())])
async def update_user_by_userid(request: UpdateUserApiRequestById, db: Session = Depends(deps.get_db), current_user: LoggedInUser = Depends(get_current_user))->UpdateUserApiResponse :
    service_request: UpdateUserServiceRequestById =ApiToServiceModelConverter().ToServiceModelUpdateById(request)
    service_response: UpdateUserServiceResponse =  TokenService().UserUpdateById(db, service_request, current_user)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model

@user.get('/list', response_model=UserListApiResponse, response_model_exclude_unset=True)
async def get_user_list( db: Session = Depends(deps.get_db))->UserListApiResponse :
    service_response:UserListServiceResponse =  TokenService().GetUserList(db)
    api_response_model = ServiceToApiModelConverter().ToAPIModelUserList(service_response)
    return api_response_model



@user.get('/me', response_model=UserApiResponse, response_model_exclude_unset=True, dependencies=[Depends(JWTBearer())])
async def get_current_user_data( db: Session = Depends(deps.get_db), current_user: LoggedInUser = Depends(get_current_user))->UserApiResponse :   
    service_response: UserServiceResponse =  TokenService().GetSelfUser(db, current_user)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model

@user.get('/{id}', response_model=UserApiResponse, response_model_exclude_unset=True)
async def get_user_details( id: str, db: Session = Depends(deps.get_db))->UserApiResponse :
    service_request: UserServiceRequest =ApiToServiceModelConverter().ToServiceModelGetUser(id)
    service_response: UserServiceResponse =  TokenService().GetUser(db, service_request)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model
