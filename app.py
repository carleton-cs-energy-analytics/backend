import os
import psycopg2

from flask import Flask

app = Flask(__name__)

CONN = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')

cursor = CONN.cursor()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/buildings')
def get_all_buildings():
    try:
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(a)))
        FROM (
            SELECT * FROM Buildings
            ) AS a;
        """)
        result = cursor.fetchall()[0]
        print(result)
        return result

    except Exception as e:
        # TODO: do something with exceptions
        raise e


if __name__ == '__main__':
    app.run()
