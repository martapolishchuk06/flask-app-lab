from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_bp
    from .users import users_bp
    from .products import products_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)

    from app.posts import post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app