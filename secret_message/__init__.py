# 发表主题贴
from flask import Blueprint, jsonify, g, request
from Model import session, Post, Subject, SecMessage, User
from conf import status

SecMessage = Blueprint('SecMessage', __name__)

@SecMessage.route("/getSecMessage", methods=["POST"])
def getSecMessage(tid):
    uid = request.form.get('uid', None)
    msgs = session.query(SecMessage).filter(SecMessage.uid_receiver == uid).all()
    messages = []
    for msg in msgs:
        name_sender = session.query(User).filter(User.uid==msg.uid_sender).first()
        name_sender = name_sender.username
        name_receiver = session.query(User).filter(User.uid==msg.uid_receiver).first()
        name_receiver = name_sender.username
        message = {"from_id": msg.uid_sender,
                   "from_name": name_sender,
                   "to_id": msg.uid_receiver,
                   "to_name": name_receiver,
                   "text": msg.message,
                   }
        messages.append(message.copy())
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": '私信获取成功',
        'data': messages
    }
    return jsonify(result)

@SecMessage.route("/sendSecMessage", methods=["POST"])
def sendSecMessage():
    message = request.form.get('message', None)
    to_uid = request.form.get("to_uid", None)
    from_uid = g.uid
    if message is None or to_uid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    from_name = session.query(User).filter(User.uid==from_uid).first()
    to_name = session.query(User).filter(User.uid==to_uid).first()
    if to_name is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    new_message = SecMessage(uid_sender=from_uid, uid_receiver=to_uid, message=message, name_sender=from_name, name_receiver=to_name)
    session.add(new_message)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "发送成功！",
    }
    return jsonify(result)

