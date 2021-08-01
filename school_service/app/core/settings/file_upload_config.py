from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, BaseModel, SecretStr
from pydantic import BaseSettings, PostgresDsn, validator

class AzureConfig(BaseSettings):
    sas_token = "?sv=2020-02-10&ss=bfqt&srt=sco&sp=rwdlacuptfx&se=2024-03-31T20:08:38Z&st=2021-06-09T12:08:38Z&spr=https,http&sig=sSDYEHTKPgcnVEkY%2BLaVkw%2BWJz1cDKDgRHinUpfDLOI%3D"
    MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=tooliqadevstorage;AccountKey=azqUWBL3rXexTM/v3hwmvVb+4SH7haGWLvH1+xjG3m6CpD/U6VP9ix7Bn8edjNVF9KnbdTsvda/8RfoDQaEZOw==;EndpointSuffix=core.windows.net"
