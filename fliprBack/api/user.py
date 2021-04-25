from flask import request, Blueprint
from flask.globals import session
from fliprBack.constants import *
from fliprBack.config import tzone
from fliprBack.auth import validate_token, get_token
from fliprBack.response import make_response, HTTPStatus
from fliprBack.models import *
import datetime

userBP = Blueprint('userApi', __name__)


@userBP.route('/register', methods=['POST'])
def useraction():
    if request.method == 'POST':
        data = request.json
        return save_new_user(data=data)
    else:
        return make_response("method not allowed", HTTPStatus.MethodNotAllowed)


def save_new_user(data):
    required_parameters = ['username', 'password', 'contact_number']
    if (set(required_parameters)-data.keys()):
        return make_response("Missing Input.", HTTPStatus.BadRequest)
    from server import SQLSession
    session = SQLSession()
    connection = session.connection()
    _usr = session.query(User).filter_by(
        contact_number=data['contact_number']).first()
    if _usr:
        return make_response("Contact already exist.", HTTPStatus.BadRequest)
    user = session.query(User).filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data['password'],
            contact_number=data['contact_number'],
            registered_on=datetime.datetime.utcnow()+tzone,
            last_updated_on=datetime.datetime.utcnow()+tzone
        )
        try:
            session.add(new_user)
            session.commit()
            session.close()
            connection.close()
            payload = {
                "username": data['username']
            }
            return make_response("User created successfully.", HTTPStatus.Success, payload)
        except Exception as e:
            session.close()
            connection.close()
            return make_response("Problem saving in db", HTTPStatus.InternalError)
    else:
        session.close()
        connection.close()
        return make_response("User already exists", HTTPStatus.BadRequest)


@userBP.route('/', methods=['GET'])
def get_my_detail():
    auth_token = request.headers.get('auth-token')
    if not auth_token:
        return make_response("No 'auth-token' in header", HTTPStatus.NoToken)
    valid_token, usr_ = validate_token(auth_token)
    if valid_token:
        result = {
            "username": usr_.username,
            "varified": usr_.varified,
            "contact_number": usr_.contact_number,
        }
        return make_response("Detail of the user", status_code=HTTPStatus.Success, payload=result)
    else:
        if usr_ == Constants.InvalidToken:
            return make_response("Invalid token", HTTPStatus.InvalidToken)
        elif usr_ == Constants.TokenExpired:
            return make_response("Token expired.", HTTPStatus.InvalidToken)
        else:
            return make_response("User not verified", HTTPStatus.UnAuthorised)


@userBP.route('/login', methods=['POST'])
def login():
    data = request.json
    token = get_token(data)
    required_parameters = ['username', 'password']
    if (set(required_parameters)-data.keys()):
        return make_response("Missing Input.", HTTPStatus.BadRequest)
    if token == Constants.NoUser:
        return make_response("User not exist", HTTPStatus.NotFound)
    elif token == Constants.NotVerified:
        return make_response("User not verified/blocked.", HTTPStatus.NotVerified)
    elif token == Constants.InvalidCredential:
        return make_response("Invalid Credential", HTTPStatus.UnAuthorised)
    else:
        res = {
            "username": data['username'],
            "auth-token": token
        }
        return make_response(msg="Token success", status_code=HTTPStatus.Success, payload=res)


@userBP.route('/myteam', methods=['GET'])
def myteam():
    auth_token = request.headers.get('auth-token')
    if not auth_token:
        return make_response("No 'auth-token' in header", HTTPStatus.NoToken)
    valid_token, usr_ = validate_token(auth_token)
    if valid_token:
        match_id = request.args.get('match_id', None, type=int)
        if match_id == None:
            return make_response("Query parameter 'match_id' missing.", HTTPStatus.BadRequest)
        from server import SQLSession
        session = SQLSession()
        connection = session.connection()
        my_team = session.query(Userteam).join(Userteam.playermatch).filter(
            Userteam.user_id == usr_.id).filter(Playermatch.match_id == match_id).all()
        payload = {
            "team": {}
        }
        credit_spent = 0
        for i in my_team:
            p_name = i.playermatch.player.playername
            p_credit = i.playermatch.player.credit_value
            payload['team'][p_name] = p_credit
            credit_spent += p_credit
        payload['credit_spent'] = credit_spent
        session.close()
        connection.close()
        return make_response("Detail of the user Team", status_code=HTTPStatus.Success, payload=payload)
    else:
        if usr_ == Constants.InvalidToken:
            return make_response("Invalid token", HTTPStatus.InvalidToken)
        elif usr_ == Constants.TokenExpired:
            return make_response("Token expired.", HTTPStatus.InvalidToken)
        else:
            return make_response("User not verified", HTTPStatus.UnAuthorised)
