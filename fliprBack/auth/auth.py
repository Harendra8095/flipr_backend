import jwt
import os
import datetime

from fliprBack.constants import Constants
from fliprBack.config import *
from fliprBack.models import User

from dotenv import load_dotenv
load_dotenv()


def validate_token(token):
    '''
    Return bollean 
    true -> valid token.... 
    false -> Invalid token....
    takes dict as input having field "token"
    '''
    try:
        from server import SQLSession
        session = SQLSession()
        conn = session.connection()
        try:
            d = jwt.decode(token, os.environ.get('SECRET_KEY'))
            usr = d['email']
            user_ = session.query(User).filter_by(email=usr).first()
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
    from server import SQLSession
    session = SQLSession()
    connection = session.connection()
    user = session.query(User).filter_by(email=data['email']).first()
    print("IN GET Token:: ", user)
    session.close()
    connection.close()
    if not user:
        return Constants.NoUser
    else:
        if user.check_password(data.get('password')):
            return jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=Token_Validity)}, os.environ.get('SECRET_KEY')).decode('UTF-8')
        else:
            return Constants.InvalidCredential
