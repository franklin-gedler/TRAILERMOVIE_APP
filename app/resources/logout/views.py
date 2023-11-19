
from flask import Blueprint

logout = Blueprint("logout", __name__)
####

@logout.route("/logout")
def main():
    return "endpoint logout"