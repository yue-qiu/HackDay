from flask import Flask
from Config import config
from auth import Auth, auth_login, cors
from message import Message
from subject import Sub
from user_info import UserInfo
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    Message.before_request(auth_login)
    Sub.before_request(auth_login)
    Message.after_request(cors)
    Sub.after_request(cors)
    UserInfo.after_request(cors)
    app.register_blueprint(Auth, url_prefix="/auth")
    app.register_blueprint(Message, url_prefix="/message")
    app.register_blueprint(Sub, url_prefix="/sub")
    app.register_blueprint(UserInfo, url_prefix="/user_info")
    return app


app = create_app()
CORS(app, supports_credentials=True)
