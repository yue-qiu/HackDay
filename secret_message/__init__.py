# 发表主题贴
from flask import Blueprint, jsonify, g, request
from Model import session, Post, Subject, SecMessage, User, Comment
from conf import status

SecretMessage = Blueprint('SecretMessage', __name__)

@SecretMessage.route("/getSecMessage", methods=["POST"])
def getSecMessage():
    uid = g.uid
    msgs = session.query(SecMessage).filter(SecMessage.uid_receiver == uid or SecMessage.uid_sender== uid).all()
    messages = []
    for msg in msgs:
        message = {"from_id": msg.uid_sender,
                   "from_name": msg.name_sender,
                   "to_id": msg.uid_receiver,
                   "to_name": msg.name_receiver,
                   "text": msg.message,
                   "msg_type": msg.msg_type
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
    to_uid = request.form.get("to_uid", None)
    from_uid = g.uid
    msg_type = int(request.form.get("msg_type", 0))
    if msg_type == 0:
        message = request.form.get('message', None)
    else:
        message = request.files.get('message', None)
    if message is None or to_uid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    intimate1 = session.query(Comment).filter(Comment.uid_commentee==from_uid, Comment.uid_commenter==to_uid).first()
    intimate2 = session.query(Comment).filter(Comment.uid_commentee==to_uid, Comment.uid_commenter==from_uid).first()
    if intimate1 is None or intimate2 is None or min(intimate1.counter, intimate2.counter) < 30:
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
    if msg_type == 1:
        if intimate1 is None or intimate2 is None or min(intimate1.counter, intimate2.counter) < 50:
            ret = {
                'code': status.get('PERMISSION'),
                'MESSAGE': '亲密度未达到文本私信要求'
            }
            return jsonify(ret)
        pic_info = requests.post('http://api.cugxuan.cn:8080/upload', files={'file': message})
        pic_info = pic_info.json()
        if pic_info['code'] == 200:
            pic_url = 'http://pic1.cugapp.com/' + pic_info['name']
            message = pic_url
        else:
            ret = {
                'code': status.get('ERROR'),
                'MESSAGE': '无法上传图片'
            }
            return jsonify(ret)
    new_message = SecMessage(uid_sender=from_uid, uid_receiver=to_uid, message=message, name_sender=from_name.username, name_receiver=to_name.username, msg_type=msg_type)
    session.add(new_message)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "发送成功！",
    }
    return jsonify(result)

