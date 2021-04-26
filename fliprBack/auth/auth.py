import jwt
import os
import datetime

from fliprBack.constants import Constants
from fliprBack.config import *
from fliprBack.models import User

from dotenv import load_dotenv
load_dotenv()


def validate_token(token):
    try:
        from server import SQLSession
        session = SQLSession()
        conn = session.connection()
        try:
            d = jwt.decode(token, os.environ.get('SECRET_KEY'))
            usr = d['username']
            user_ = session.query(User).filter_by(username=usr).first()
        except Exception as e:
            session.close()
            conn.close()
        session.close()
        conn.close()
        if not user_:
            return False, Constants.InvalidToken
        else:
            return True, user_
    except:
        return False, Constants.TokenExpired


def get_token(data):
    print(os.environ.get('SECRET_KEY'))
    from server import SQLSession
    session = SQLSession()
    connection = session.connection()
    user = session.query(User).filter_by(username=data['username']).first()
    print("IN GET Token:: ", user.username)
    session.close()
    connection.close()
    if not user:
        return Constants.NoUser
    else:
        if user.check_password(data.get('password')):
            return jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=Token_Validity)}, os.environ.get('SECRET_KEY')).decode('UTF-8')
        else:
            return Constants.InvalidCredential
