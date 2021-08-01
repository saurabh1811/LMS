import datetime
from pydantic import BaseModel, Field, validator

class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime = None
    
    @validator("created_at", pre=True)
    def default_datetime(
        cls,
        value: datetime.datetime,
    ) -> datetime.datetime:
        return value or datetime.datetime.now()
    
class BaseServiceResponseModel(BaseModel):
    error : bool = False
    message: str = ""

class BaseServiceRequestModel(BaseModel):
    userid: int =0