from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
config = Config('.env') 


oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    },
    client_id ="72765080457-7qvebsthkb1842skg7m3idmdddo576nu.apps.googleusercontent.com",
    client_secret ="3nM-m1YvM5halYgVDCpMl5yw"
)