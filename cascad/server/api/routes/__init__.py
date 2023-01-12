from .home import home_bp
# from .blockchain import  blockchain_bp


def init_app(app): 
    app.register_blueprint(home_bp)
    # app.register_blueprint(blockchain_bp, url_prefix='blockchain')