from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import datetime

engine = create_engine("mysql+pymysql://root:123456@192.168.1.111/hackday", encoding='utf-8', echo=True)
base = declarative_base()
base.metadata.create_all(engine)  # 创建表结构
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(base):
    __tablename__ = 'user_information'  # 表名
    uid = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
    register_time = Column(DateTime, default=datetime.datetime.utcnow)
    avatar_url = Column(String(255))
    phone = Column(String(15))
    email = Column(String(20))
    qq = Column(String(12))
    wechat = Column(String(15))
    is_active = Column(Integer)


class Post(base):
    __tablename__ = 'post_information'  # 表名
    tid = Column(Integer)
    content = Column(String(65535))
    comment_floor = Column(Integer)
    fid = Column(Integer)
    post_time = Column(DateTime, default=datetime.datetime.utcnow)
    like = Column(Integer)
    pid = Column(Integer, primary_key=True)
    uid = Column(Integer)


class Subject(base):
    __tablename__ = 'subject_information'  # 表名
    tid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    title = Column(String(255))
    post_time = Column(DateTime, default=datetime.datetime.utcnow)


class Comment(base):
    __tablename__ = 'comment_information'  # 表名
    id = Column(Integer, primary_key=True)
    uid_commenter = Column(Integer)
    uid_commentee = Column(Integer)
    counter = Column(Integer)

class SecMessage(base):
    __tablename__ = 'secret_message_information'  # 表名
    id = Column(Integer, primary_key=True)
    uid_sender = Column(Integer)
    uid_receiver = Column(Integer)
    message = Column(String(255))
    name_sender = Column(String(255))
    name_receiver = Column(String(255))
    time = Column(DateTime, default=datetime.datetime.utcnow)
    msg_type = Column(Integer)
