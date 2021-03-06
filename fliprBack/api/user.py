from fliprBack.models.matchModel import Scorehistory
from flask import request, Blueprint
from flask.globals import session
from fliprBack.constants import *
from fliprBack.config import tzone
from fliprBack.auth import validate_token, get_token
from fliprBack.response import make_response, HTTPStatus
from fliprBack.models import *
import datetime
import json

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
            "id": usr_.id,
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
            "team": []
        }
        credit_spent = 0
        for i in my_team:
            p_name = i.playermatch.player.playername
            p_credit = i.playermatch.player.credit_value
            payload['team'].append(
                {
                    "player_id": i.playermatch.player_id,
                    "playername": p_name,
                    "credit_value": p_credit,
                    "captain": i.captain,
                    "vice_captain": i.vice_captain
                }
            )
            credit_spent += p_credit
        payload["credit_spent"] = credit_spent
        payload['match_id'] = match_id
        session.close()
        connection.close()
        return make_response("success", status_code=HTTPStatus.Success, payload=payload)
    else:
        if usr_ == Constants.InvalidToken:
            return make_response("Invalid token", HTTPStatus.InvalidToken)
        elif usr_ == Constants.TokenExpired:
            return make_response("Token expired.", HTTPStatus.InvalidToken)
        else:
            return make_response("User not verified", HTTPStatus.UnAuthorised)


@userBP.route('/scoreboard', methods=['GET'])
def scoreboard():
    auth_token = request.headers.get('auth-token')
    if not auth_token:
        return make_response("No 'auth-token' in header", HTTPStatus.NoToken)
    valid_token, usr_ = validate_token(auth_token)
    if valid_token:
        match_id = request.args.get('match_id', None, type=int)
        if match_id == None:
            return make_response("Query parameter 'match_id' missing.", HTTPStatus.BadRequest)
        from server import SQLSession, get
        session = SQLSession()
        connection = session.connection()
        my_team = session.query(Userteam).join(Userteam.playermatch).filter(
            Userteam.user_id == usr_.id).filter(Playermatch.match_id == match_id).all()
        p_list = []
        if my_team == None:
            return make_response("No Team created for this match", HTTPStatus.BadRequest)
        vc = ''
        c = ''
        for i in my_team:
            p_name = i.playermatch.player.playername
            p_list.append(p_name)
            if i.captain:
                c = p_name
                print(c)
            if i.vice_captain:
                vc = p_name
                print(vc)
        last_ball = get(match_id)
        print(last_ball)
        score = 0
        payload = {
            "team": []
        }
        if last_ball:
            all_player = session.query(Livescore).filter_by(ball=last_ball).join(
                Livescore.playermatch).filter_by(match_id=match_id).all()
        else:
            all_player = session.query(Scorehistory).join(
                Scorehistory.playermatch).filter_by(match_id=match_id).all()
        for i in all_player:
            p_name = i.playermatch.player.playername
            if p_name in p_list:
                poin = i.points
                if p_name == vc:
                    poin = i.points*1.5
                if p_name == c:
                    poin = i.points*2
                payload['team'].append({
                        "playername": p_name,
                        "points" : poin
                    })
        for i in payload['team']:
            score += i['points']
        payload["total_score"] = score
        session.close()
        connection.close()
        return make_response("Success", status_code=HTTPStatus.Success, payload=payload)
    else:
        if usr_ == Constants.InvalidToken:
            return make_response("Invalid token", HTTPStatus.InvalidToken)
        elif usr_ == Constants.TokenExpired:
            return make_response("Token expired.", HTTPStatus.InvalidToken)
        else:
            return make_response("User not verified", HTTPStatus.UnAuthorised)


@userBP.route('/assign', methods=['POST'])
def assign():
    auth_token = request.headers.get('auth-token')
    if not auth_token:
        return make_response("No 'auth-token' in header", HTTPStatus.NoToken)
    valid_token, usr_ = validate_token(auth_token)
    data = request.json
    required_parameters = ['match_id', 'player_id', 'role']
    if (set(required_parameters)-data.keys()):
        return make_response("Missing Input.", HTTPStatus.BadRequest)
    if not valid_token:
        if usr_ == Constants.InvalidToken:
            return make_response("Invalid token", HTTPStatus.InvalidToken)
        elif usr_ == Constants.TokenExpired:
            return make_response("Token expired.", HTTPStatus.InvalidToken)
        else:
            return make_response("User not verified", HTTPStatus.UnAuthorised)
    else:
        from server import SQLSession
        session = SQLSession()
        connection = session.connection()
        match_id = data['match_id']
        player_id = data['player_id']
        player = session.query(Userteam).join(Userteam.playermatch).filter(
            Userteam.user_id == usr_.id).filter(Playermatch.match_id == match_id).all()
        if data['role'].lower()=='c':
            for i in player:
                if i.playermatch.player_id==player_id:
                    i.captain = True
                    i.vice_captain = False
                    print(player_id, i.captain)
                else:
                    i.captain = False
        elif data['role'].lower()=='vc':
            for i in player:
                if i.playermatch.player_id==player_id:
                    i.vice_captain = True
                    i.captain = False
                    print(player_id, i.vice_captain)
                else:
                    i.vice_captain = False
        session.commit()
        session.close()
        connection.close()
        return make_response("success", HTTPStatus.Success)
