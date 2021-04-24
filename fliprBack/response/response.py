from flask import jsonify


def make_response(msg, status_code, payload=None):
    if payload is None:
        response_object = {
            "message": msg
        }
    else:
        response_object = {
            "message": msg,
            "payload": payload
        }
    return jsonify(response_object), status_code
