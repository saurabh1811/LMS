from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import  auth_routes as api_router
from app.api.routes import  user_routes as user_router
from app.api.Errors.universal_exception_handler import catch_exceptions_middleware
from app.api.Errors.validation_exception_handler import ValidationErrorLoggingRoute
from app.core.settings import JWTConfig

from starlette.middleware.sessions import SessionMiddleware


def get_application() -> FastAPI:
    application = FastAPI(
                title="eAacharya Auth API",
                description="API's for future.",
                version="1.0.0",
        )
    # add_middlewares(application)
    # application.add_middleware(SessionMiddleware, secret_key=JWTConfig().secret_key)
    add_auth_routes(application)
    add_user_routes(application)

    application.router.route_class = ValidationErrorLoggingRoute

    return application

def add_middlewares(application:FastAPI):
    application.add_middleware(
                    CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                     )
    
    application.middleware('http')(catch_exceptions_middleware)
    return application

def add_user_routes(application:FastAPI):
    application.include_router(user_router.user, prefix='/api/v1/user', tags=['User'])
    return application 

def add_auth_routes(application:FastAPI):
    application.include_router(api_router.auth, prefix='/api/v1/auth', tags=['Auth'])
    return application    



