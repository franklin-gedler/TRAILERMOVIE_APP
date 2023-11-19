"""Flask app creation."""

from flask import Flask
from app.resources import inicio, peliculas, series, contactanos, login, admin, logout, health, search, rating
from config import Secrets

ACTIVE_ENDPOINTS = (inicio, peliculas, series, 
                    contactanos, login, admin, logout, health, search, rating)


def create_app():
    """Create Flask app."""
    app = Flask(__name__)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    app.config.from_object(Secrets)

    app.static_folder = "static"

    # register each active blueprint
    [app.register_blueprint(blueprint) for blueprint in ACTIVE_ENDPOINTS]

    return app
