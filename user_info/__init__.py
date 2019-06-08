# 发表主题贴
from flask import Blueprint, jsonify, g, request, session as ses
from Model import session, Post, Subject, User
from conf import status
import requests

UserInfo = Blueprint('UserInfo', __name__)


@UserInfo.route("/getUserInfo", methods=["POST"])
def getUserInfo():
    uid = request.form.get('uid')
    if uid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    user = session.query(User).filter(User.uid == uid).first()
    if user is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '未找到该用户'
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
        print(pic_info)
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
