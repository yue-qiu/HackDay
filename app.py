from flask import Flask
from Config import config
from auth import Auth, auth_login
from post import Post
from subject import Sub


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    Auth.before_request(auth_login)
    Post.before_request(auth_login)
    Sub.before_request(auth_login)
    app.register_blueprint(Auth, url_prefix="/auth")
    app.register_blueprint(Post, url_prefix="/post")
    app.register_blueprint(Sub, url_prefix="/sub")
    return app


app = create_app()
