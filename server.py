from flask import Flask
from dotenv import load_dotenv
load_dotenv()
from fliprBack.config import DbEngine_config
from fliprBack import create_db_engine, create_db_sessionFactory
from fliprBack.api import *
from flask_cors import CORS
from fliprBack.models import *
from test.dbtest import populate_dummy



engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)

createTables(engine)
populate_dummy()


app = Flask(__name__)
app.config.from_object(DbEngine_config())

CORS(app, supports_credentials=True)


@app.route('/')
def get():
    return "<h1> Hello, Welcome to backend of Flipr-ipl </h1>"


app.register_blueprint(userBP, url_prefix='/user')
app.register_blueprint(teamBP, url_prefix='/team')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
