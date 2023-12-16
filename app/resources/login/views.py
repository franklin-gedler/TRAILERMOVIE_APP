
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import requests
#from flask_login import login_user, current_user
from app.modules.form import LoginForm
#from app.modules.auth import User
from config import Secrets

login = Blueprint("login", __name__)
####

@login.route("/login", methods=['GET', 'POST'])
def main():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        base_url = Secrets.BASE_URL_API

        # Realizar la solicitud a tu API para obtener el token
        response = requests.post(f'{base_url}/login', json={'username': username, 'password': password})

        if response.json().get('status'):
            session['user_role'] = response.headers.get('X-User-Role')
            response = response.json()
            session['jwt_token'] = response['access_token']
            session['current_user'] = username
            
            return redirect(url_for('dashboard.main'))
        
        form.process() # Limpia el form
        flash(response.json().get('error'), 'error')
        return redirect(url_for('login.main'))

    return render_template('login.html', title='Login', form=form, current_user=session.get('current_user', None), user_role=session.get('user_role', None))

    # Implementacion de flask-login se cambio por flask-sessions
    '''form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Realizar la solicitud a tu API para obtener el token
        response = requests.post('http://tu-api.com/login', json={'username': username, 'password': password})

        if response.status_code == 200 and response.json().get('status'):
            user = User()
            user.id = username
            login_user(user)

            # Guardar el token en la sesión del usuario
            session['jwt_token'] = response.json()['access_token']

            return redirect(url_for('dashboard'))

    #return render_template('login.html', title='admin', form=form, current_user=current_user)'''
