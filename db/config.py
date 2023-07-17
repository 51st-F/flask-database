import cx_Oracle
import pymysql
import psycopg2
import pandas as pd
from flask import jsonify

def connect_oracle(sql: str, **kwargs):
    conn_str = kwargs['conn_str']
    try:
        db = cx_Oracle.connect(
            f'''{conn_str['username']}/{conn_str['password']}@{conn_str['host']}/{conn_str['database']}'''
        )

        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_dict = [dict(zip(columns, row)) for row in result]
        cursor.close()
        db.close()

        return jsonify(result_dict)

    except cx_Oracle.IntegrityError as e:
        error_obj, = e.args
        print(sql)
        print("Error Code:", error_obj.code)
        print("Error Message:", error_obj.message)


def connect_mysql(sql: str, **kwargs):
    conn_str = kwargs['conn_str']
    try:
        db = pymysql.connect(
            host=conn_str['host'],
            port=int(conn_str['port']),
            database=conn_str['database'],
            user=conn_str['username'],
            password=conn_str['password'],
            connect_timeout=10,
            read_timeout=60,
        )

        with db.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result_dict = [dict(zip(columns, row)) for row in result]
            cursor.close()
            db.close()

            return jsonify(result_dict)

    except pymysql.Error as e:
        print(sql)
        print(e.args[0], e.args[1])


def connect_psql(sql: str, **kwargs):
    conn_str = kwargs['conn_str']
    try:
        db = psycopg2.connect(
            host=conn_str['host'],
            port=int(conn_str['port']),
            database=conn_str['database'],
            user=conn_str['username'],
            password=conn_str['password'],
        )

        with db.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result_dict = [dict(zip(columns, row)) for row in result]
            cursor.close()
            db.close()

            return jsonify(result_dict)
        
    except psycopg2.Error as e:
        print(sql)
        print(e.args)
