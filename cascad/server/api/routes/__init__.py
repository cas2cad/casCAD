from .home import home_bp
from .chain import chain
from .auth import auth_bp
# from .blockchain import  blockchain_bp


def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(chain)
    app.register_blueprint(auth_bp)
    # app.register_blueprint(blockchain_bp, url_prefix='blockchain')
    return app
