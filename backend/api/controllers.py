from flask import Blueprint
from backend.database.models import CONN

api = Blueprint('api', __name__)

@api.route('/buildings')
def get_all_buildings():
    try:
        CONN.cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(a)))
        FROM (
            SELECT * FROM Buildings
            ) AS a;
        """)
        result = CONN.cursor.fetchall()[0]
        print(result)
        return result

    except Exception as e:
        # TODO: do something with exceptions
        raise e