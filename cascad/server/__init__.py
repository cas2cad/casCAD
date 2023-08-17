from flask import Flask
from flask_login.utils import login_user
from cascad.server.config import config
from cascad.server.api import routes
from cascad.server.api import dashboard
from cascad.settings import BASE_DIR
from flask_bootstrap import Bootstrap
import os
from pyecharts.globals import CurrentConfig
from jinja2 import Environment, FileSystemLoader
from flask_login import LoginManager
from cascad.models.datamodel import User
# import flask_login

template_folder = os.path.join(BASE_DIR,  'server', 'templates')
static_folder = os.path.join(BASE_DIR,  'server', 'static')

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader(template_folder))
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


def create_app(config_name='development'):
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.config.from_object(config[config_name])
    login_manager.init_app(app)
    app.secret_key = 'EFSDUFX16SDSDUE' 
    config[config_name].init_app(app)
    Bootstrap(app)
    # login_manager = flask_login.LoginManager()
    # login_manager.init_app(app)

    app = routes.init_app(app)
    app = dashboard.init_dashboard(app)
    login_manager.login_view = 'auth_bp.login_post'

    return app

