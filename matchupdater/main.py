import json
import datetime
import time
import redis
import os
from dotenv import load_dotenv
load_dotenv()
from matchupdaterBack.models import *
from matchupdaterBack import create_db_engine, create_db_sessionFactory
from matchupdaterBack.config import DbEngine_config
from matchupdaterBack.api import *



engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
print('redis://',REDIS_HOST,':',REDIS_PORT)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

if __name__ == "__main__":
    i = 1
    time.sleep(2)
    while True:
        session = SQLSession()
        connection = session.connection()
        cur_date = session.query(Day).filter_by(id=i).first().avail_date
        livematch(cur_date)
        i += 1
        time.sleep(7200)
