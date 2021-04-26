from flask import Flask
from dotenv import load_dotenv
load_dotenv()
from fliprBack.config import DbEngine_config
from fliprBack import create_db_engine, create_db_sessionFactory
from fliprBack.api import *
from flask_cors import CORS
from fliprBack.models import *
import redis
import os
from test.dbtest import populate_dummy



engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

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


@app.route('/')
def get():
    return "<h1> Hello, Welcome to backend of Flipr-ipl </h1>\
        <h2> API_DOC: http://65.2.157.158:8080 </h2>\
        <h2> FRONTEND: http://65.2.157.158:80</h2>"


app.register_blueprint(userBP, url_prefix='/user')
app.register_blueprint(teamBP, url_prefix='/team')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
