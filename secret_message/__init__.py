# 发表主题贴
from flask import Blueprint, jsonify, g, request
from Model import session, Post, Subject, SecMessage, User, Comment
from conf import status

SecretMessage = Blueprint('SecretMessage', __name__)

@SecretMessage.route("/getSecMessage", methods=["POST"])
def getSecMessage():
    uid = g.uid
    msgs = session.query(SecMessage).filter(SecMessage.uid_receiver == uid).all()
    messages = []
    for msg in msgs:
        message = {"from_id": msg.uid_sender,
                   "from_name": msg.name_sender,
                   "to_id": msg.uid_receiver,
                   "to_name": msg.name_receiver,
                   "text": msg.message,
                   }
        messages.append(message.copy())
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": '私信获取成功',
        'data': messages
    }
    return jsonify(result)

@SecretMessage.route("/sendSecMessage", methods=["POST"])
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
    intimate1 = session.query(Comment).filter(Comment.uid_commentee==from_uid, Comment.uid_commenter==to_uid).first()
    intimate1 = intimate1.count
    intimate2 = session.query(Comment).filter(Comment.uid_commentee==to_uid, Comment.uid_commenter==from_uid).first()
    intimate2 = intimate2.count
    intimate = min(intimate1, intimate2)
    if intimate < 30:
        ret = {
            'code': status.get('PERMISSION'),
            'MESSAGE': '亲密度未达到文本私信要求'
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
    new_message = SecMessage(uid_sender=from_uid, uid_receiver=to_uid, message=message, name_sender=from_name.username, name_receiver=to_name.username)
    session.add(new_message)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "发送成功！",
    }
    return jsonify(result)

