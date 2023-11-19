import psycopg2
from config import Secrets

class DataTransform:
    def __init__(self, iterable):
        self.iterable = iterable

    def transform_data(self):
        return [{'video': row[0], 'img': row[1], 'alt': row[2], 'details': row[3].replace('\n', '')} for row in self.iterable]

class Handler_DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(Secrets.DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise DatabaseConnectionError("Error de conexión a la base de datos")
        
    def get_data(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            raise DatabaseQueryError("Error al ejecutar la query")
        
    def update_data(self, query: str, params: tuple = None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise DatabaseQueryError("Error al actualizar datos en la base de datos")

    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()


class DatabaseConnectionError(Exception):
    pass

class DatabaseQueryError(Exception):
    pass