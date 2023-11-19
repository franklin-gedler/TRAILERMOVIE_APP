"""views __init__ module."""

from app.resources.inicio.views import inicio
from app.resources.peliculas.views import peliculas
from app.resources.series.views import series
from app.resources.contactanos.views import contactanos
from app.resources.login.views import login
from app.resources.admin.views import admin
from app.resources.logout.views import logout
from app.resources.health.views import health
from app.resources.search.views import search
from app.resources.rating.views import rating

__all__ = [
    "inicio", 
    "peliculas",
    "series",
    "contactanos",
    "login",
    "admin",
    "logout",
    "health",
    "search",
    "rating"
]
