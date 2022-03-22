from flask import Flask
from cascad.server.config import config
from cascad.server import routes


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    routes.init_app(app)

    return app
