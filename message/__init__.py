# 发表主题贴
from flask import Blueprint, jsonify, g, request
from Model import session, User, Post, Subject
from conf import status

Message = Blueprint('Message', __name__)


@Message.route("/view/<string:tid>", methods=["GET"])
def view(tid):
    floors = session.query(Post).filter(Post.tid == tid).all()
    messages = []
    for floor in floors:
        message = {"content": floor.content,
                   "comment_floor": floor.comment_floor,
                   "post_time": floor.post_time,
                   "like": floor.like, }
        messages.append(message.copy())
    result = {
        "code": status.get("SUCCESS"),
        "messages": messages,
    }
    return jsonify(result)


@Message.route("/post", methods=["POST"])
def post():
    title = request.form.get('title', None)
    uid = g.uid
    if title is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    new_subject = Subject(uid=uid, title=title)
    session.add(new_subject)
    session.commit()

    content = request.form.get("content")
    floor = request.form.get("comment_floor", "1")
    message = Post(tid=new_subject.tid, content=content, comment_floor=floor, fid=1, like=0)
    session.add(message)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "发帖成功！",
    }
    return jsonify(result)
