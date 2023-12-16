
from flask import Blueprint, render_template, request, jsonify, session
from app.modules.db import Handler_DB, DataTransform

search = Blueprint("search", __name__)
####

@search.route("/search", methods=['POST'])
def main():
    db = Handler_DB()
    termino_busqueda = request.form.get('search_input')
    
    query_base = "SELECT video_id, link_img, name_tipo, details FROM table WHERE name_tipo ILIKE %s"

    query_peliculas = query_base.replace('name_tipo', 'name_pelicula').replace('table', 'peliculas')
    peliculas_data = DataTransform(db.get_data(query_peliculas, ('%' + termino_busqueda + '%',))).transform_data()

    query_series = query_base.replace('name_tipo', 'name_serie').replace('table', 'series')
    series_data = DataTransform(db.get_data(query_series, ('%' + termino_busqueda + '%',))).transform_data()

    return jsonify({'moviesData': peliculas_data, 'seriesData': series_data})

@search.route("/resultsearch")
def resultsearch():
    return render_template('search.html', title='Results', current_user=session.get('current_user', None))