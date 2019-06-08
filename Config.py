import os

base = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'UniqueHackDay'
    DEBUG = True
    basedir = base
    db_host = "192.168.1.111"
    db_username = "root"
    db_password = "123456"
    db_port = "3306"
    db_name = "hackday"


config = {
    "Develop": Config,
}

