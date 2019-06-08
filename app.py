from flask import Flask
from Config import config
from auth import Auth, auth_login


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    app.register_blueprint(Auth, url_prefix="/auth")
    Auth.before_request(auth_login)
    return app


app = create_app()



