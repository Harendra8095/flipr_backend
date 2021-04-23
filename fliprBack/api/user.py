from flask import Blueprint

userBP = Blueprint('userApi', __name__)


@userBP.route('/', methods=['GET'])
def get_my_detail():
    return '<h1> Hi, Harry <h1>'
