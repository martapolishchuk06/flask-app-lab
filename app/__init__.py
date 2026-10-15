from flask import Flask

app = Flask(__name__)

from . import views
from . import users_bp
from . import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)