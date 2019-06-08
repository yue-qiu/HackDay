from flask import Flask
from Config import config
from auth import Auth, auth_login, cors
from post import Post
from subject import Sub
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    Post.before_request(auth_login)
    Sub.before_request(auth_login)
    Post.after_request(cors)
    Sub.after_request(cors)
    app.register_blueprint(Auth, url_prefix="/auth")
    app.register_blueprint(Post, url_prefix="/post")
    app.register_blueprint(Sub, url_prefix="/sub")
    return app


app = create_app()
CORS(app, supports_credentials=True)
