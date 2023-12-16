
from flask import Blueprint, render_template, request, jsonify, session
from app.modules.db import Handler_DB, DataTransform

peliculas = Blueprint("peliculas", __name__)
####

@peliculas.route("/peliculas", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        db = Handler_DB()

        query_peliculas = "SELECT video_id, link_img, name_pelicula, details FROM peliculas ORDER BY id DESC"
        peliculas_data = DataTransform(db.get_data(query_peliculas)).transform_data()

        return jsonify({'moviesData': peliculas_data})
    
    return render_template('peliculas.html', title='Peliculas', current_user=session.get('current_user', None))