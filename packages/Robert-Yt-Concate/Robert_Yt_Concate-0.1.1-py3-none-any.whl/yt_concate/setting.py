import os
from dotenv import load_dotenv

load_dotenv()
API_KEYS = os.getenv('API_KEY3')

DOWNLOADS_DIRS = 'downloads'
CAPTIONS_DIRS = os.path.join(DOWNLOADS_DIRS, 'captions')
VIDEOS_DIRS = os.path.join(DOWNLOADS_DIRS, 'videos')
OUTPUT_DIRS = os.path.join(DOWNLOADS_DIRS, 'output')
