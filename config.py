import os
from dotenv import load_dotenv

load_dotenv()
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM')
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')