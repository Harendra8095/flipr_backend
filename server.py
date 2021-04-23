from flask import Flask
from fliprBack.config import DbEngine_config
from fliprBack import create_db_engine, create_db_sessionFactory
from fliprBack.api import *

from dotenv import load_dotenv
load_dotenv()

engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)

app = Flask(__name__)
app.config.from_object(DbEngine_config())


@app.route('/')
def get():
    return "<h1> Hello, Welcome to backend of Flipr-ipl </h1>"


app.register_blueprint(userBP, url_prefix='/user')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
