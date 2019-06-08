import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String,DateTime
import datetime

class User(base):
    __tablename__ = 'user_information' #表名
    uid = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(64))
    register_time = Column(DateTime, default=datetime.datetime.utcnow)

class Post(base):
    __tablename__ = 'post_information' #表名
    tid = Column(Integer, primary_key=True)
    content = Column(String(65535))
    comment = Column(String(65535))
    fid = Column(Integer, primary_key=True)
    post_time = Column(DateTime, default=datetime.datetime.utcnow)

class Subject(base):
    __tablename__ = 'subject_information' #表名
    tid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    title = Column(String(255))
    register_time = Column(DateTime, default=datetime.datetime.utcnow)

class DB:
    def __init__():
        #创建连接
        engine=create_engine("mysql+pymysql://root:123456@localhost/hackday",encoding='utf-8',echo=True)
        #生成orm基类
        base=declarative_base()
        base.metadata.create_all(engine) #创建表结构
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
