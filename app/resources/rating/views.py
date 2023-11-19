
from flask import Blueprint, render_template, request, jsonify
from app.modules.db import Handler_DB, DataTransform

rating = Blueprint("rating", __name__)
####

@rating.route("/rating", methods=['GET', 'POST'])
def main():
    db = Handler_DB()
    if request.method == 'POST':
        termino_busqueda = request.form.get('name')
        rating_select = request.form.get('rating')
        
        query_base = "SELECT total_average, vote_count FROM table WHERE column LIKE %s"

        for table_column in [['peliculas', 'name_pelicula'], ['series', 'name_serie']]:
            query = query_base.replace('table', table_column[0]).replace('column', table_column[1])
            data_rating = db.get_data(query, ('%' + termino_busqueda + '%',))
            total_average, vote_count = data_rating[0]

            if total_average and vote_count:

                vote_count+=1
            
                try:
                    total_average = int(total_average)
                except:
                    total_average = float(total_average)
            
                total_average += int(rating_select)

                result = total_average / 2

                if result.is_integer():
                    new_total_average = str(int(result))
                else:
                    if list(str(result))[2] == '0':
                        new_total_average = ''.join(list(str(result))[:1])
                    else:
                        new_total_average = ''.join(list(str(result))[:3])
                
                name_table = table_column[0]
                name_column = table_column[1]

                # Construir la consulta de actualización dinámicamente
                update_query = f"UPDATE {name_table} SET total_average = %s, vote_count = %s WHERE {name_column} LIKE %s"

                # Actulizo los valores en la db
                db.update_data(update_query, (new_total_average, vote_count, '%' + termino_busqueda + '%'))

                return jsonify({'value': new_total_average})
            
            else:
                # Entra aca en caso de que exista el termino de busqueda en la base de datos pero las columnas: total_average y vote_count sean None o null

                name_table = table_column[0] # tabla donde se encontro el termino de busqueda
                name_column = table_column[1] # columna donde se encontro el termino de busqueda
                vote_count = 1

                # Construir la consulta de actualización dinámicamente
                update_query = f"UPDATE {name_table} SET total_average = %s, vote_count = %s WHERE {name_column} LIKE %s"

                # Actulizo los valores en la db
                db.update_data(update_query, (rating_select, vote_count, '%' + termino_busqueda + '%'))

                return jsonify({'value': rating_select})

    ##### GET #####    
    termino_busqueda = request.args.get('name')
    query_base = "SELECT total_average FROM table WHERE column LIKE %s"

    for table_column in [['peliculas', 'name_pelicula'], ['series', 'name_serie']]:
        query = query_base.replace('table', table_column[0]).replace('column', table_column[1])
        total_average = db.get_data(query, ('%' + termino_busqueda + '%',))
        if total_average:
            return jsonify({'total_average': total_average[0][0]})
    
    return jsonify({'total_average': None})

