"""Flask app creation."""

from flask import Flask
#from app.resources import inicio, peliculas, series, contactanos, login, admin, logout, health, search, rating
from config import Secrets
from app.resources import ACTIVE_ENDPOINTS
#from flask_login import LoginManager
#from app.modules.auth import User

#ACTIVE_ENDPOINTS = (inicio, peliculas, series, 
#                    contactanos, login, admin, logout, health, search, rating)

def create_app():
    """Create Flask app."""
    app = Flask(__name__)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    app.config.from_object(Secrets)

    app.static_folder = "static"

    # register each active blueprint
    [app.register_blueprint(blueprint) for blueprint in ACTIVE_ENDPOINTS]

    # Implementacion de flask-login se cambio por flask-sessions
    '''login_manager = LoginManager(app)
    login_manager.login_view = "login.main"  # Vista de inicio de sesión
    #login_manager.login_view = url_for("login.main")
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = User()
        user.id = user_id
        return user'''

    return app
