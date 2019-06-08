from flask import Blueprint, request, jsonify, session as ses
import hashlib
from Model import session, User
from conf import status

Auth = Blueprint('Auth', __name__, url_prefix="/auth")


@Auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        user = session.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username, password=hash.hexdigest())
            session.add(user)
            session.commit()
            result = {
                "code": status.get("SUCCESS"),
                "message": "SUCCESS",
            }
            return jsonify(result)
    result = {
        "code": status.get("FAIL"),
        "message": "FAIL",
    }
    return jsonify(result)


@Auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        user = session.query(User).filter(User.username == username, User.password == hash.hexdigest()).first()
        if user and not ses.get(user.uid, None):
            ses["uid"] = user.uid
            result = {
                "code": status.get("SUCCESS"),
                "MESSAGE": "SUCCESS",
            }
            return jsonify(result)
    result = {
        "code": status.get("FAIL"),
        "MESSAGE": "FAIL",
    }
    return jsonify(result)

