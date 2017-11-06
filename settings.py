import os
import pathlib
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(os.path.dirname(__file__))
TIMEZONE = 'America/Sao_Paulo'

# Load environment variables from `.env` file (if exists)
ENV_FILE = BASE_DIR / '.env'
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# Database
MONGODB_URI = os.environ['MONGODB_URI']
# On Mlab, the URI has the Default DB already
DEFAULT_DB = MONGODB_URI.split('/')[-1]

# Twitter
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# Bit.ly
BITLY_TOKEN = os.environ['BITLY_TOKEN']

# Facebook
FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
