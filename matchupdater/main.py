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


def get(key, decode=True):
    """set decode to False when value stored as a string"""
    value = redis_client.get(key)
    if not decode:
        return value
    if value is not None:
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value


if __name__ == "__main__":
    time.sleep(240)
    while True:
        i = get('match_id')
        session = SQLSession()
        connection = session.connection()
        # cur_date = session.query(Day).filter_by(id=i).first().avail_date
        livematch(i)
        redis_client.set("match_id", i+1)
        print("Next match starting in 5 Hours")
        time.sleep(2400)
