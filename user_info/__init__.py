# 发表主题贴
from flask import Blueprint, jsonify, g, request, session as ses
from Model import session, User, Comment, Subject
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
    uid = int(uid)
    that_uid = int(that_uid)
    print(uid, that_uid)
    if uid != that_uid:
        intimate1 = session.query(Comment).filter(Comment.uid_commentee == that_uid,
                                                  Comment.uid_commenter == uid).first()
        intimate2 = session.query(Comment).filter(Comment.uid_commentee == uid,
                                                  Comment.uid_commenter == that_uid).first()
        if intimate1 is None or intimate2 is None or min(intimate1.counter, intimate2.counter) < 70:
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
            'avatar': user.avatar_url,
            'phone': user.phone,
            'email': user.email,
            'qq': user.qq,
            'wechat': user.wechat
        }
    }
    print(ret)
    return jsonify(ret)


@UserInfo.route("/setUserInfo", methods=["POST"])
def setUserInfo():
    username = request.form.get('username', None)
    pic_file = request.files.get('new_pic', None)
    phone = request.files.get('new_phone', None)
    email = request.files.get('new_email', None)
    qq = request.files.get('new_qq', None)
    wechat = request.files.get('new_wechat', None)
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
    if phone is not None:
        user.phone = phone
    if email is not None:
        user.email = email
    if qq is not None:
        user.qq = qq
    if wechat is not None:
        user.wechat = wechat
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


@UserInfo.route("/getUid", methods=['GET'])
def getUid():
    uid = ses.get('uid', None)
    print(uid)
    if uid is None:
        result = {
            "code": status.get("ERROR"),
            "MESSAGE": "获取UID失败",
            "uid": -1,
        }
        print(result)
        return jsonify(result)
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": "获取UID成功",
        "uid": uid,
    }
    print(result)
    return jsonify(result)


@UserInfo.route("/getUidByUsername", methods=["POST"])
def getUidByUsername():
    username = request.form.get('username', None)
    if username is None:
        result = {
            "code": status.get("ERROR"),
            "MESSAGE": "获取UID失败",
        }
        return jsonify(result)
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        result = {
            "code": status.get("ERROR"),
            "MESSAGE": "不存在该用户",
        }
        return jsonify(result)
    uid = user.uid
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": "获取UID成功",
        "uid": uid,
    }
    return jsonify(result)


@UserInfo.route("/history")
def history():
    passages = session.query(Subject).filter(Subject.uid == g.uid).all()
    infos = []
    for passage in passages:
        info = {"tid": passage.tid, "title": passage.title, "post_time": passage.post_time}
        infos.append(info.copy())
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": "获取个人历史发帖纪录成功",
        "infos": infos
    }
    return jsonify(result)

