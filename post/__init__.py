# 发表主题贴
from flask import Blueprint
from Model import session, User, Post, Subject

Post = Blueprint('Post', __name__)

def postSubject(uid, title):
    new_subject = Subject(uid=uid, title=title)
    session.add(new_subject)
    session.commit()

def deleteSubject(tid):
    subject = session.query(Subject).filter_by(tid=tid).first()
    if subject is not None:
        session.delete(subject)
        session.commit()
        return True
    return False

def modSubject(tid, title):
    subject = session.query(Subject).filter_by(tid=tid).first()
    if subject is not None:
        subject.title = title
        session.commit()
        return True
    return False

def getSubList(page_index): # page_index start from 1
    page_size = 10
    return session.query(Subject).order_by(Subject.tid.desc()).slice((page_index - 1) * page_size, page_index * page_size)
