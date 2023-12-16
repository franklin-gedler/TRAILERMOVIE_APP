
from flask import Blueprint, session, redirect, url_for, render_template, flash, request
#from flask_login import login_required
from app.modules.form import FormContainer
from app.modules.funtions import HandlerApi, InvalidTokenError, generate_payload
from config import Secrets
import requests

dashboard = Blueprint("dashboard", __name__)
####

@dashboard.route("/dashboard", methods=['GET', 'POST'])
#@login_required
def main():
    
    form = FormContainer()

    try:
        api_handler = HandlerApi(form)
    except InvalidTokenError as e:
        flash(str(e), 'error')
        return redirect(url_for('logout.main'))

    if form.validate_on_submit():
        
        action = request.form.get('action', None)

        if action == 'add_pelicula_serie':
                    
            payload = {
                form.create_form_pelicula_serie.name_type.data: form.create_form_pelicula_serie.name_type_input.data,
                'video_id': form.create_form_pelicula_serie.video_id.data,
                'link_img': form.create_form_pelicula_serie.link_img.data,
                'details': form.create_form_pelicula_serie.details.data,
            }

            return api_handler.handle_request(endpoint='create', method='post', payload=payload)

        elif action == 'get_pelicula_serie':

            name = form.get_form_pelicula_serie.name_pelicula_serie.data

            params = {'name': name}

            return api_handler.handle_request(endpoint='read', method='get', params=params)

        elif action == 'update_pelicula_serie':

            name = form.update_form_pelicula_serie.name_pelicula_serie.data

            campos = ['video_id', 'link_img', 'new_name', 'details']

            payload = generate_payload(form.update_form_pelicula_serie, campos)

            if not payload:
                flash('Al menos uno de los campos; video_id, link_img, new_name o details debe contener datos.', 'error')
                return redirect(url_for('dashboard.main'))

            return api_handler.handle_request(endpoint='update', method='put', params={'name': name}, payload=payload)

        elif action == 'delete_pelicula_serie':

            tipo = form.delete_form_pelicula_serie.name_type.data
            name = form.delete_form_pelicula_serie.name_type_input.data

            params = {tipo: name}

            return api_handler.handle_request(endpoint='delete', method='delete', params=params)

        elif action == 'add_user':
            payload = {
                'username': form.create_form_user.username.data,
                'password': form.create_form_user.password.data,
                'allow': form.create_form_user.allow.data,
            }

            return api_handler.handle_request(endpoint='create/user', method='post', payload=payload)

        elif action == 'get_user':

            username = form.get_form_user.username.data

            params = {'username': username}

            return api_handler.handle_request(endpoint='read/user', method='get', params=params)
            
        elif action == 'update_user':

            user = form.update_form_user.user.data

            campos = ['username', 'password', 'allow']

            payload = generate_payload(form.update_form_user, campos)

            if not payload:
                flash('Al menos uno de los campos; Nuevo Nombre, Nueva Password o Nuevo Allow debe contener datos.', 'error')
                return redirect(url_for('dashboard.main'))
            
            return api_handler.handle_request(endpoint='update/user', method='put', params={'user': user}, payload=payload)

        elif action == 'delete_user':
            user = form.delete_form_user.user.data

            return api_handler.handle_request(endpoint='delete/user', method='delete', params={'user': user})

    return render_template(
        'dashboard.html', 
        title='Dashboard', 
        form=form,
        current_user=session.get('current_user', None), 
        user_role=session.get('user_role', None)
    )