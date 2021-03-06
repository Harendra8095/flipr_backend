from flask import Flask
from dotenv import load_dotenv
load_dotenv()
from fliprBack.config import DbEngine_config
from fliprBack import create_db_engine, create_db_sessionFactory
from fliprBack.api import *
from flask_cors import CORS
from fliprBack.models import *
import redis
import json
import os
from test.dbtest import populate_dummy



engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)
REDIS_HOST = os.environ.get('REDIS_HOST') if os.environ.get('REDIS_HOST') else "redis"
REDIS_PORT = os.environ.get('REDIS_PORT') if os.environ.get('REDIS_PORT') else "6379"
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
print("REDIS_URL: redis://", REDIS_HOST, ":", REDIS_PORT)

def clearlivetable():
    session = SQLSession()
    session.query(Livescore).delete()
    session.commit()
    session.close()

# clearlivetable()
# creaatteTables(engine)
# popule_dummy()


app = Flask(__name__)
app.config.from_object(DbEngine_config())

CORS(app, supports_credentials=True)

def get(key, decode=True):
    """set decode to False when value stored as a string"""
    from server import redis_client
    value = redis_client.get(key)
    if not decode:
        return value
    if value is not None:
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError:
            return value


@app.route('/')
def main():
    return "<h1> Hello, Welcome to backend of Flipr-ipl </h1>\
        <h2> API_DOC: http://65.2.157.158:8080 </h2>\
        <h2> FRONTEND: http://65.2.157.158:80</h2>"


app.register_blueprint(userBP, url_prefix='/user')
app.register_blueprint(teamBP, url_prefix='/team')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
