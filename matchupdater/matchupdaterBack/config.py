from pytz import timezone
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

class DbEngine_config():
    DB_DIALECT = os.environ.get('DB_DIALECT') or 'postgresql'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = os.environ.get('DB_PORT') or '5432'
    DB_USER = os.environ.get('DB_USER') or 'postgres'
    DB_PASS = os.environ.get('DB_PASS') or 'postgres'
    DB_NAME = os.environ.get('DB_NAME') or 'flipr'
    if(os.environ.get('TEST') == '1'):
        DB_NAME = 'flipr_test'
    DB_URL = f'{DB_DIALECT}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    print(DB_URL)
    SQLALCHEMY_DATABASE_URI = DB_URL
