from flask import Flask
from cascad.server.config import config
from cascad.server import routes
from cascad.settings import BASE_DIR
from flask_bootstrap import Bootstrap
import os
from pyecharts.globals import CurrentConfig
from jinja2 import Markup, Environment, FileSystemLoader

template_folder = os.path.join(BASE_DIR,  'server', 'templates')
static_folder = os.path.join(BASE_DIR,  'server', 'static')

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader(template_folder))

def create_app(config_name='development'):
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    Bootstrap(app)

    routes.init_app(app)

    return app
