import sqlite3
import os

from flask import Flask, request, abort, flash
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
TABLES_NAMES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"
DB_NAME = 'my_data.db'


def print_ans(filename, cursor) -> str:
    ans = ""
    cursor.execute(f'''pragma table_info({filename});''')
    for i in cursor.fetchall():
        ans += str(i) + "\n"
    return ans


def isExists(filename, cur) -> bool:
    cur.execute(TABLES_NAMES_SQL)
    tables = cur.fetchall()
    return (filename,) in tables


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def work():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 404

        filename = secure_filename(file.filename)
        filename = filename.rsplit('.', 1)[0].lower()

        if '.' in filename and filename.rsplit('.', 1)[1].lower() != 'csv':
            return "This format is not support", 404

        conn = sqlite3.connect(DB_NAME)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if isExists(filename, conn.cursor()):
            return "Table with this name already exists", 404
        else:
            file.save(path)
            table_name = filename.rsplit('.', 1)[0].lower()
            data = pd.read_csv(path)
            data = data.dropna()
            data = data.apply(pd.to_numeric, errors='ignore')
            data.to_sql(table_name, conn, if_exists='append', index=False)
            os.remove(path)

        return "OK", 200

    if request.method == 'GET':
        conn = sqlite3.connect(DB_NAME)

        ans = ''
        print(request.headers)
        if request.headers.get('file') is None:
            cursor = conn.cursor()
            cursor.execute(TABLES_NAMES_SQL)
            tables = cursor.fetchall()
            if len(tables) == 0:
                return "NO TABLES", 200
            for table, in tables:
                ans += 'TABLE:\t' + table + '\n'
                ans += print_ans(table, conn.cursor())
        else:
            filename = secure_filename(request.headers['file'])
            filename = filename.rsplit('.', 1)[0].lower()
            if not isExists(filename, conn.cursor()):
                return "There's no such this table", 404

            sql = f''' SELECT * FROM {filename} '''

            if request.headers.get('filter'):
                filters = request.headers['filter'].split(';')
                for i, val in enumerate(filters):
                    if i == 0:
                        sql += 'WHERE ' + val
                    else:
                        sql += ' and ' + val

            if request.headers.get('sort'):
                filters = request.headers['sort'].split(';')
                for i, val in enumerate(filters):
                    if i == 0:
                        sql += ' ORDER BY \"' + val + '\" ASC'
                    else:
                        sql += ' , ' + val
            sql += ';'
            print(sql)
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                ans += str(row) + "\n"
        conn.close()
        return ans, 200

    if request.method == 'DELETE':
        conn = sqlite3.connect(DB_NAME)

        if request.headers.get('file') is None:
            cursor = conn.cursor()
            cursor.execute(TABLES_NAMES_SQL)
            for table, in cursor.fetchall():
                cursor2 = conn.cursor()
                cursor2.execute(f"DROP TABLE {table}")
                conn.commit()
            conn.close()
            return "DELETE ALL", 200
        else:
            file = request.headers['file']
            filename = secure_filename(file)
            if '.' in filename:
                filename = filename.rsplit('.', 1)[0].lower()
            if not isExists(filename, conn.cursor()):
                return "There's no such this table", 404

            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE {filename}")
            conn.commit()
            conn.close()
            return "DELETE "+filename, 200


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
