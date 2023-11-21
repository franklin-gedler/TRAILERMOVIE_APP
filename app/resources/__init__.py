"""views __init__ module."""

import os
from importlib import import_module

# path endpoints
base_dir = "app/resources"

# get all names of subdirectories in app/resources
subdirectories = [sub_dir for sub_dir in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, sub_dir)) and not (sub_dir.startswith("__") or sub_dir.startswith("."))]

ACTIVE_ENDPOINTS = []
for folder in subdirectories:
    module_name = f'app.resources.{folder}.views'
    module = import_module(module_name)
    blueprint = getattr(module, folder)
    ACTIVE_ENDPOINTS.append(blueprint)


'''from app.resources.inicio.views import inicio
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
'''