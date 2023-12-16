
from flask import Blueprint, redirect, url_for, render_template, request, jsonify, session
from app.modules.db import Handler_DB, DataTransform

inicio = Blueprint("inicio", __name__)
####

@inicio.route('/')
def redirigir_a_inicio():
    return redirect(url_for('inicio.main'))

@inicio.route("/inicio", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        db = Handler_DB()

        query_base = "SELECT video_id, link_img, name_tipo, details FROM table ORDER BY id DESC LIMIT 6"
        
        query_peliculas = query_base.replace('name_tipo', 'name_pelicula').replace('table', 'peliculas')
        peliculas_data = DataTransform(db.get_data(query_peliculas)).transform_data()


        query_series = query_base.replace('name_tipo', 'name_serie').replace('table', 'series')
        series_data = DataTransform(db.get_data(query_series)).transform_data()

        return jsonify({'moviesData': peliculas_data, 'seriesData': series_data})

    return render_template('inicio.html', title='Página de Inicio', current_user=session.get('current_user', None))