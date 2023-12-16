
from flask import Blueprint, render_template, request, jsonify, session
from app.modules.db import Handler_DB, DataTransform

series = Blueprint("series", __name__)
####

@series.route("/series", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        db = Handler_DB()

        query_series = "SELECT video_id, link_img, name_serie, details FROM series ORDER BY id DESC"
        series_data = DataTransform(db.get_data(query_series)).transform_data()

        return jsonify({'seriesData': series_data})
    
    return render_template('series.html', title='Series', current_user=session.get('current_user', None))