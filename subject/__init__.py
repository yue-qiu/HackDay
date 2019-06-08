# 发表主题贴
from flask import Blueprint, request, jsonify, session as ses
from Model import session, User, Post, Subject
from conf import status

Sub = Blueprint('Sub', __name__)

@Sub.route('/postSubject', methods=['POST'])
def postSubject():
    title = request.form.get('title', None)
    uid = ses.get("uid", None)
    if title is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    new_subject = Subject(uid=uid, title=title)
    session.add(new_subject)
    session.commit()
    ret = {
        'code': status.get("SUCCESS"),
        'MESSAGE': '发帖成功'
    }
    return jsonify(ret)

@Sub.route('/deleteSubject', methods=['POST'])
def deleteSubject(tid):
    tid = request.form.get('tid', None)
    uid = ses.get("uid", None)
    if tid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    subject = session.query(Subject).filter_by(tid==tid and uid==uid).first()
    if subject is not None:
        session.delete(subject)
        session.commit()
        return True
    return False
    

@Sub.route('/modSubject', methods=['POST'])
def modSubject(tid, title):
    tid = request.form.get('tid', None)
    uid = ses.get("uid", None)
    if tid is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    subject = session.query(Subject).filter_by(tid==tid and uid==uid).first()
    subject = session.query(Subject).filter_by(tid=tid).first()
    if subject is not None:
        subject.title = title
        session.commit()
        return True
    return False

@Sub.route('/getSubList', methods=['POST'])
def getSubList(page_index): # page_index start from 1
    page_size = 10
    return session.query(Subject).order_by(Subject.tid.desc()).slice((page_index - 1) * page_size, page_index * page_size)
