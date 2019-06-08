# 发表主题贴
from flask import Blueprint, request, jsonify, session as ses
from Model import session, User, Post, Subject
from conf import status

Sub = Blueprint('Sub', __name__)


@Sub.route('/modSubject', methods=['POST'])
def modSubject():
    tid = request.form.get('tid', None)
    title = request.form.get('title', None)
    uid = ses.get("uid", None)
    if tid is None or title is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    subject = session.query(Subject).filter(Subject.tid == tid).first()
    ret = {
        'code': status.get('ERROR'),
        'MESSAGE': '找不到该贴'
    }
    if subject is not None:
        subject.title = title
        session.commit()
        ret['code'] = status.get('SUCCESS')
        ret['MESSAGE'] = '修改成功'
    return jsonify(ret)


@Sub.route('/getSubList', methods=['POST'])
def getSubList():  # page_index start from 1
    page_size = 10
    page_index = request.form.get('page', None)
    if page_index is None:
        ret = {
            'code': status.get('ERROR'),
            'MESSAGE': '参数不合法'
        }
        return jsonify(ret)
    page_index = int(page_index)
    subjectList = session.query(Subject).order_by(Subject.tid.desc()).slice((page_index - 1) * page_size,
                                                                            page_index * page_size)
    data = list()
    for v in subjectList:
        user = session.query(User).filter(User.uid == v.uid).first()
        username = '匿名' if user is None else user.username
        avater = 'http://pic1.cugapp.com/FikstAllXLweowBEXpy5FQxPd8td.jpg' if user is None else user.avatar_url
        threads = session.query(Post).filter(Post.tid == v.tid).count()
        item = {
            'tid': v.tid,
            'username': username,
            'title': v.title,
            'post_time': v.post_time,
            'threads': threads,
            'avatar': avater,
        }
        data.append(item)
    ret = {
        'code': status.get('SUCCESS'),
        'MESSAGE': "获取列表成功",
        'data': data
    }
    return jsonify(ret)


@Sub.route('/getSubCount', methods=['POST'])
def getSubCount():
    subject_count = session.query(Subject).count();
    ret = {
        'code': status.get('SUCCESS'),
        'MESSAGE': "获取主题贴总数成功",
        'data': subject_count
    }
    return jsonify(ret)
