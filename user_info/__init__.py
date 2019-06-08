# 发表主题贴
from flask import Blueprint, jsonify, g, request, session as ses
from Model import session, User, Comment
from conf import status
import requests

UserInfo = Blueprint('UserInfo', __name__)


@UserInfo.route("/getUserInfo", methods=["POST"])
def getUserInfo():
    that_uid = request.form.get('uid', None)
    uid = ses.get('uid', None)
    if that_uid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    user = session.query(User).filter(User.uid == that_uid).first()
    if user is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '未找到该用户'
        }
        return jsonify(ret)
    if uid != that_uid:
        intimate1 = session.query(Comment).filter(Comment.uid_commentee==that_uid, Comment.uid_commenter==uid).first()
        intimate2 = session.query(Comment).filter(Comment.uid_commentee==uid, Comment.uid_commenter==that_uid).first()
        if intimate1 is None or intimate2 is None or min(intimate1, intimate2) < 70:
            ret = {
                'code': status.get('PERMISSION'),
                'MESSAGE': '亲密度未达到查看个人信息要求'
            }
            return jsonify(ret)
    ret = {
        "code": status.get("SUCCESS"),
        "messages": '获取用户信息成功',
        'data': {
            'uid': uid,
            'username': user.username,
            'avatar': user.avatar_url
        }
    }
    return jsonify(ret)
        

@UserInfo.route("/setUserInfo", methods=["POST"])
def setUserInfo():
    username = request.form.get('username', None)
    pic_file = request.files.get('new_pic', None)
    uid = ses.get('uid')
    user = session.query(User).filter(User.uid == uid).first()
    if user is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '未找到该用户'
        }
        return jsonify(ret)
    if username is not None:
        user.username = username
    if pic_file is not None:
        pic_info = requests.post('http://api.cugxuan.cn:8080/upload', files={'file': pic_file})
        pic_info = pic_info.json()
        if pic_info['code'] == 200:
            pic_url = 'http://pic1.cugapp.com/' + pic_info['name']
            user.avatar_url = pic_url
        else:
            ret = {
                'code': status.get('ERROR'),
                'MESSAGE': '无法上传图片'
            }
            return jsonify(ret)
    session.commit()
    ret = {
        "code": status.get("SUCCESS"),
        "messages": '修改用户信息成功'
    }
    return jsonify(ret)


@UserInfo.route("/hot/<string:id>", methods=["GET"])
def Hot(id):
    relation = session.query(Comment).filter(Comment.uid_commentee == id, Comment.uid_commenter == g.uid).first()
    if relation:
        hot = relation.counter
    else:
        hot = 0
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": "亲密度获取成功",
        "result": hot,
    }
    return jsonify(result)
