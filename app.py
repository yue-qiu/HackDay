from flask import Flask
from Config import config
from auth import Auth


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["Develop"])
    app.register_blueprint(Auth)
    return app


app = create_app()



