
from flask import Blueprint, session, redirect, url_for

logout = Blueprint("logout", __name__)
####

@logout.route("/logout")
def main():
    session.pop('jwt_token', None)
    session.pop('current_user', None)
    session.pop('user_role', None)

    return redirect(url_for('login.main'))