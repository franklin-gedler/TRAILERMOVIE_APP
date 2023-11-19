
from flask import Blueprint

admin = Blueprint("admin", __name__)
####

@admin.route("/admin")
def main():
    return "endpoint admin"