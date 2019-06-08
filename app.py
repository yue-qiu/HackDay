from flask import Flask
from Config import config
from auth import Auth, auth_login, cors
from message import Message
from subject import Sub
from user_info import UserInfo
from secret_message import SecMessage
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    Message.before_request(auth_login)
    Sub.before_request(auth_login)
    UserInfo.before_request(auth_login)
    SecMessage.before_request(auth_login)
    app.register_blueprint(Auth, url_prefix="/auth")
    app.register_blueprint(Message, url_prefix="/message")
    app.register_blueprint(Sub, url_prefix="/sub")
    app.register_blueprint(UserInfo, url_prefix="/user_info")
    app.register_blueprint(SecMessage, url_prefix="/sec_message")
    return app


app = create_app()
CORS(app, supports_credentials=True)
