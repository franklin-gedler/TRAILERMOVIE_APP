
from flask import Blueprint

login = Blueprint("login", __name__)
####

@login.route("/login")
def main():
    return "endpoint login"