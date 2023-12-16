import jwt
import requests
from config import Secrets
from flask import redirect, url_for, flash, session, request, render_template

def generate_payload(data, campos):
    payload = {}

    for campo in campos:
        dato = getattr(data, campo).data
        if dato is not None and dato != '':
            payload[campo] = dato
    
    return payload


class HandlerApi:
    def __init__(self, form):
        self.form = form
        self.jwt_token = session.get('jwt_token', None)
        if self.jwt_token is None or not self.validate_token(self.jwt_token):
            raise InvalidTokenError('Please, Re-login')
        self.headers = {'Authorization': f'Bearer {self.jwt_token}'}
        self.base_url = Secrets.BASE_URL_API
        
    def validate_token(self, token):
        try:
            # Verifica la firma y desencripta el token
            jwt.decode(token, Secrets.SECRET_KEY, algorithms=['HS256'])
            # Si la decodificación es exitosa, el token es válido
            return True
        except jwt.ExpiredSignatureError:
            # Token expirado
            return False
        except jwt.InvalidTokenError:
            # Token inválido
            return False

    def handle_request(self, endpoint, method, payload=None, params=None):

        url = f"{self.base_url}/{endpoint}"

        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            url = f"{url}?{query_string}"

        response = requests.request(method, url, json=payload, headers=self.headers).json()

        return self.handle_response(response)

    def handle_response(self, response):

        if response.get('status', None):
            if response.get('message', None):
                self.form.process() # Limpia el form
                flash(response.get('message'), 'success')
                return redirect(url_for('dashboard.main'))
            else:
                if 'username' in response.get('result'):
                    self.form.process()
                    return render_template(
                        'dashboard.html', 
                        title='Dashboard', 
                        form=self.form,
                        current_user=session.get('current_user', None), 
                        user_role=session.get('user_role', None),
                        user_info=response.get('result')
                    )
                else:
                    self.form.process()
                    return render_template(
                        'dashboard.html', 
                        title='Dashboard', 
                        form=self.form,
                        current_user=session.get('current_user', None), 
                        user_role=session.get('user_role', None),
                        pelicula_serie_info=response.get('result')
                    )
                
        elif 'msg' in response:
            flash(response['msg'], 'error')
            return redirect(url_for('logout.main'))
        
        else:
            flash(response.get('error', 'Error Desconocido'), 'error')
            return redirect(url_for('dashboard.main'))
        
class InvalidTokenError(Exception):
    pass
