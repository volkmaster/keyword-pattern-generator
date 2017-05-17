import os
from dotenv import load_dotenv
load_dotenv('.env')


__author__ = 'Ziga Vucko'


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
PRINTER_NAMES = os.environ.get('PRINTER_NAMES').split(',')
DOCUMENT_NAME = os.environ.get('DOCUMENT_NAME')
