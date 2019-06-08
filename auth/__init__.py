from flask import Blueprint, request, jsonify, session as ses, g, make_response
import hashlib
from Model import session, User
from conf import status

Auth = Blueprint('Auth', __name__)


@Auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username and password:
        hash = hashlib.md5()
        hash.update(password.encode(encoding='utf-8'))
        user = session.query(User).filter(User.username == username).first()
        if not user:
            user = User(username=username, password=hash.hexdigest(), avatar_url='http://pic1.cugapp.com/FikstAllXLweowBEXpy5FQxPd8td.jpg')
            session.add(user)
            session.commit()
            result = {
                "code": status.get("SUCCESS"),
                "message": "注册成功",
            }
            return jsonify(result)
    result = {
        "code": status.get("FAIL"),
        "message": "注册失败，用户名已存在",
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
        if user and not ses.get("uid", None):
            ses["uid"] = user.uid
            result = {
                "code": status.get("SUCCESS"),
                "MESSAGE": "登陆成功",
            }
            return jsonify(result)
    result = {
        "code": status.get("FAIL"),
        "MESSAGE": "登陆失败，请检查用户密码",
    }
    return jsonify(result)


def auth_login():
    g.uid = ses.get("uid", None)
    if not g.uid:
        result = {
            "code": 300,
            "MESSAGE": "未登录",
        }
        print(result)
        return jsonify(result)


def cors(resp):
    resp = make_response(resp)
    #header("Access-Control-Allow-Origin: http://localhost:9999");
    resp.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.111:5000'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Credentials'] = True
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp
