# 发表主题贴
from flask import Blueprint, jsonify, g, request
from Model import session, Post, Subject, User
from conf import status
from user_info import Comment

Message = Blueprint('Message', __name__)


@Message.route("/view/<string:tid>", methods=["GET"])
def view(tid):
    floors = session.query(Post).filter(Post.tid == tid).all()
    messages = []
    for floor in floors:
        commentee = session.query(Post).filter(Post.fid == floor.comment_floor).first()
        commentee_name = session.query(User).filter(User.uid == commentee.uid).first()
        message = {"content": floor.content,
                   "comment_floor": floor.comment_floor,
                   "comment_name": commentee_name,
                   "post_time": floor.post_time,
                   "like": floor.like,
                   "fid": floor.fid,
                   }
        messages.append(message.copy())
    result = {
        "code": status.get("SUCCESS"),
        "messages": messages,
    }
    return jsonify(result)


@Message.route("/post", methods=["POST"])
def post():
    title = request.form.get('title', None)
    content = request.form.get("content")
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

    message = Post(tid=new_subject.tid, content=content, comment_floor=1, fid=1, like=0, uid=g.uid)
    session.add(message)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "发帖成功！",
    }
    return jsonify(result)


@Message.route("/comment", methods=["POST"])
def comment():
    tid = request.form.get("tid")
    content = request.form.get("content")
    comment_floor = request.form.get("comment_floor", 1)
    last_floor = session.query(Post).order_by(Post.fid.desc()).first()
    message = Post(tid=tid, content=content, comment_floor=int(comment_floor), fid=last_floor.fid + 1, like=0,
                   uid=g.uid)
    session.add(message)
    commentee = session.query(Post).filter(Post.fid == comment_floor).first()
    relation = session.query(Comment).filter(Comment.uid_commenter == g.uid, Comment.uid_commentee == commentee.uid).first()
    if commentee.uid != g.uid:
        if relation is None:
            comment = Comment(uid_commenter=g.uid, uid_commentee=commentee.uid, counter=1)
            session.add(comment)
        elif relation.uid_commentee != g.uid:
            relation.counter += 1
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "message": "回复成功！",
    }
    return jsonify(result)


@Message.route("/delete", methods=["POST"])
def delete():
    tid = request.form.get("tid")
    subject = session.query(Subject).filter(Subject.tid == tid, Subject.uid == g.uid).first()
    if subject:
        session.delete(subject)
        floors = session.query(Post).filter(Post.tid == tid).all()
        for floor in floors:
            session.delete(floor)
    session.commit()
    result = {
        "code": status.get("SUCCESS"),
        "MESSAGE": "删除成功",
    }
    return jsonify(result)






# @Message.route("/like", methods=["POST"])
# def like():
#     tid = request.form.get("tid")
#     fid = request.form.get("fid")
#     floor = session.query(Post).filter(Post.tid == tid, Post.fid == fid).first()
#     floor.like += 1
#     session.commit()
#     result = {
#         "code": status.get("SUCCESS"),
#         "MESSAGE": "点赞成功",
#     }
#     return jsonify(result)
