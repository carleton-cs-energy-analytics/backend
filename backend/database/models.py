import os
import psycopg2
from flask import jsonify

CONN = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')


def unwrap(result):
    return jsonify(result[0][0])


class Buildings:
    @staticmethod
    def all():
        cursor = CONN.cursor()
        cursor.execute("""
                SELECT array_to_json(array_agg(row_to_json(a)))
                FROM (
                    SELECT * FROM buildings
                    ) AS a;
                """)
        return unwrap(cursor.fetchall())

    @staticmethod
    def get(id):
        cursor = CONN.cursor()
        cursor.execute("""
        SELECT array_to_json(array_agg(row_to_json(a)))
        FROM (
            SELECT * FROM buildings WHERE building_id = %s LIMIT 1      
        ) AS a;
        """, id)
        return unwrap(cursor.fetchone())


class Rooms:
    @staticmethod
    def all():
        cursor = CONN.cursor()
        cursor.execute("""
                        SELECT array_to_json(array_agg(row_to_json(a)))
                        FROM (
                            SELECT * FROM rooms
                            ) AS a;
                        """)
        return unwrap(cursor.fetchall())

    @staticmethod
    def get(id):
        cursor = CONN.cursor()
        cursor.execute("""
                SELECT array_to_json(array_agg(row_to_json(a)))
                FROM (
                    SELECT * FROM rooms WHERE room_id = %s LIMIT 1      
                ) AS a;
                """, id)
        return unwrap(cursor.fetchone())


class Tags:
    @staticmethod
    def all():
        cursor = CONN.cursor()
        cursor.execute("""
                                SELECT array_to_json(array_agg(row_to_json(a)))
                                FROM (
                                    SELECT * FROM tags
                                    ) AS a;
                                """)
        return unwrap(cursor.fetchall())

    @staticmethod
    def get_id(id):
        cursor = CONN.cursor()
        cursor.execute("""
                    SELECT array_to_json(array_agg(row_to_json(a)))
                    FROM (
                        SELECT * FROM tags WHERE tag_id = %s LIMIT 1      
                    ) AS a;
                    """, id)
        return unwrap(cursor.fetchone())
