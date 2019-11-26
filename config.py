import os, binascii
from dotenv import load_dotenv

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(APP_ROOT, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or binascii.hexlify(os.urandom(24))
    ALLOWED_EXTENSIONS = set(['txt', 'csv', 'ris'])
    SERVING_FILE = ''
    CITATIONS_RECORD = ''
    NEO4J_USERNAME=os.getenv('DB_USERNAME')
    NEO4J_PASSWORD=os.getenv('DB_PASSWORD')
    NEO4J_URL=os.getenv('DB_URL')
