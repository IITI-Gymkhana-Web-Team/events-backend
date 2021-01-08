from flask import Flask, make_response, jsonify, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import MySQLdb
import yaml
import os
from dbConfig import database_config
from commands import get_commands

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

env = ""

if env == "dev":
    dev = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
    DATABASE_URL = dev['CLEARDB_DATABASE_URL']
    PASSWORD = dev['PASSWORD']

else:
    DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL')
    PASSWORD = os.environ.get('PASSWORD')

user, password, host, db = database_config(DATABASE_URL)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db

mysql = MySQL(app)

if env == 'dev':
    app.SECRET_KEY = dev['SECRET_KEY']
else:
    app.SECRET_KEY = os.environ.get("SECRET_KEY")


def get_events(table_name='', for_editing=False):
    cur = mysql.connection.cursor()
    cur.execute('select * from ALL_EVENTS;')
    events = cur.fetchall()

    check = -2
    if table_name == 'past_events':
        check = -1
    if table_name == 'ongoing_events':
        check = 0
    if table_name == 'upcoming_events':
        check = 1

    event_list = []
    if(for_editing):
        for i in events:
            obj = {
                "id": i[0],
                "title": i[1],
                "description": i[2],
                "details": i[3],
                "date-of-event": i[4],
                "image": i[5],
                "club": i[6],
                "status": i[7]
            }
            event_list.append(obj)
    else:
        for i in events:
            if(i[7] == check):
                obj = {
                    "id": i[0],
                    "title": i[1],
                    "description": i[2],
                    "details": i[3],
                    "date-of-event": i[4],
                    "image": i[5],
                    "club": i[6],
                }
                event_list.append(obj)

    response_body = {
        "size": len(event_list),
        "events": event_list
    }
    if(for_editing == True):
        return response_body

    res = make_response(jsonify(response_body), 200)
    return res


@app.route('/')
def example():
    return render_template('details.html')


@app.route('/past')
@cross_origin()
def past():
    return get_events("past_events")


@app.route('/ongoing')
@cross_origin()
def ongoing():
    return get_events('ongoing_events')


@app.route('/upcoming')
@cross_origin()
def upcoming():
    return get_events('upcoming_events')


@app.route("/new", methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template("new.html")
    else:
        data = request.form.to_dict()
        if(data['password'] == PASSWORD):
            table_name = data['event'] + "_events"
            if data['event'] == 'past':
                status = -1
            elif data['event'] == 'ongoing':
                status = 0
            else:
                status = 1
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO ALL_EVENTS VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', {});".format(
                data['title'], data['description'], data['details'], data['date'], data['image'], data['club'], status))
            mysql.connection.commit()
            cur.close()
            return "New Event Created"

        else:
            return "Incorrect Password"


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    res = get_events('', True)
    if request.method == 'GET':
        return render_template('allEditor.html', events=res['events'], size=res['size'])

    else:
        data = request.form.to_dict()
        if(data['password'] == PASSWORD):
            commands = get_commands(data)

            cur = mysql.connection.cursor()

            for i in commands:
                try:
                    print("Executing: " + i)
                    cur.execute(i)
                except (MySQLdb.Error, MySQLdb.Warning) as e:
                    print(e)

            mysql.connection.commit()
            cur.close()

            return redirect('/')
        else:
            return "Incorrect Password"

        return 'POST'


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == 'GET':
        return render_template("verify.html", id=id)
    else:
        data = request.form.to_dict()
        if(data['password'] == PASSWORD):

            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM ALL_EVENTS WHERE ID={}".format(id))
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        else:
            return "INCORRECT PASSWORD"


if __name__ == "__main__":
    if(env == 'dev'):
        app.run(debug=True)
    else:
        app.run()
