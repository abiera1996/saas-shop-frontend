import environ, os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.environ.get("ENV") 
if ENVIRONMENT is not None:
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.'+ENVIRONMENT))
else:
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()  

# Initialize here you Credentials variable from .env
# Sample:
# SMS_API_KEY = env('SMS_API_KEY')

REDIS_LOCATION = env('REDIS_LOCATION', default='redis://127.0.0.1:6379/1')
CACHE_TIMEOUT_SECONDS = 60 * 2