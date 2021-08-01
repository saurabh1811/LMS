from fastapi import  APIRouter,Depends
from fastapi.security import (OAuth2PasswordRequestForm)
from app.api.models import ( TokenApiResponse, SignupApiResponse, SignupApiRequest
                                ,ResetPasswordApiResponse, ResetPasswordApiRequest, UpdateUserApiRequestById)
from app.api.converters import ServiceToApiModelConverter, ApiToServiceModelConverter
from app.services.auth_service import (TokenService, SignupServiceRequest, SignupServiceResponse)
from app.services.models import (TokenServiceResponse,TokenServiceRequest
                                    , ResetPasswordServiceRequest, ResetPasswordServiceResponse, TokenEmailServiceRequest)
from sqlalchemy.orm import Session
from app.api import deps
from app.helper.auth_bearer import JWTBearer, oauth2_scheme
from app.helper import LoggedInUser, get_current_user
from app.helper.auth_bearer import JWTBearer, oauth2_scheme
from fastapi import Request
from app.helper.google_auth import oauth


auth = APIRouter()



@auth.get('/google_login', response_model=TokenApiResponse, response_model_exclude_unset=True)
async def login_for_access_token_from_google(request: Request)->TokenApiResponse :
    redirect_uri = request.url_for('authen')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth.get('/authen',  response_model=TokenApiResponse, response_model_exclude_unset=True)
async def authen( request: Request, db: Session = Depends(deps.get_db))->TokenApiResponse :

    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    print (user)
    service_request:TokenEmailServiceRequest =TokenEmailServiceRequest(google_user=user)
    service_response:TokenServiceResponse =  TokenService().GoogleLogin(db, service_request)
    api_response_model = ServiceToApiModelConverter().ToAPIModel(service_response)
    return api_response_model

@auth.post('/token', response_model=TokenApiResponse, response_model_exclude_unset=True)
async def login_for_access_token( db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends())->TokenApiResponse :

    service_request:TokenServiceRequest = TokenServiceRequest(username=form_data.username,password=form_data.password, scopes= form_data.scopes)
    service_response:TokenServiceResponse =  TokenService().Login(db, service_request)
    api_response_model = ServiceToApiModelConverter().ToAPIModel(service_response)
    return api_response_model

@auth.post('/signup', response_model=SignupApiResponse, response_model_exclude_unset=True)
async def signup_new_user(request: SignupApiRequest, db: Session = Depends(deps.get_db))->SignupApiResponse :
    service_request:SignupServiceRequest =ApiToServiceModelConverter().ToServiceModel(request)
    service_response:SignupServiceResponse =  TokenService().Signup(db, service_request)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model


@auth.post("/reset-password/", response_model=ResetPasswordApiResponse, dependencies=[Depends(JWTBearer())])
async def reset_password( request: ResetPasswordApiRequest, db: Session = Depends(deps.get_db), token: str = Depends(oauth2_scheme)) -> ResetPasswordApiResponse:
    service_request:ResetPasswordServiceRequest =ApiToServiceModelConverter().ToServiceModelReset(request)
    service_request.token = token
    service_response:ResetPasswordServiceResponse =  TokenService().ResetPassword(db, service_request)
    api_response_model = ServiceToApiModelConverter().ToAPIModelSingup(service_response)
    return api_response_model

    
@auth.post('/refresh_token', response_model=TokenApiResponse, response_model_exclude_unset=True, dependencies=[Depends(JWTBearer())])
async def get_refresh_token( db: Session = Depends(deps.get_db), current_user: LoggedInUser = Depends(get_current_user))->TokenApiResponse :
    service_response: TokenServiceResponse =  TokenService().RefreshToken(db, current_user)
    api_response_model = ServiceToApiModelConverter().ToAPIModel(service_response)
    return api_response_model

    
