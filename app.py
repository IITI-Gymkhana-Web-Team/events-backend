from flask import Flask, make_response, jsonify, render_template, request
from flask_mysqldb import MySQL
import MySQLdb
import yaml
import os
from dbConfig import database_config
from test import get_commands

app = Flask(__name__)

env = "dev"

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


def get_events(table_name, for_editing=False):
    cur = mysql.connection.cursor()
    cur.execute('select * from ' + table_name + ';')
    events = cur.fetchall()
    print(len(events))

    event_list = []
    for i in events:
        obj = {
            "id": i[0],
            "title": i[1],
            "description": i[2],
            "details": i[3],
            "date-of-event": i[4],
            "image": i[5]
        }
        event_list.append(obj)
    response_body = {
        "size": len(events),
        "events": event_list
    }
    if(for_editing == True):
        return response_body

    res = make_response(jsonify(response_body), 200)
    return res


@app.route('/')
def example():
    response_body = {
        "size": 3,
        "events": [
            {
                "id": 1,
                "title": "TItle of event",
                "description": "Short description of the event",
                "details": "More details about the event",
                "date-of-event": "Date in YYYY-MM-DD format",
                "image": "image url of the link"
            },
            {
                "id": 2,
                "title": "TItle of event",
                "description": "Short description of the event",
                "details": "More details about the event",
                "date-of-event": "Date in YYYY-MM-DD format",
                "image": "image url of the link"
            },
            {
                "id": 3,
                "title": "TItle of event",
                "description": "Short description of the event",
                "details": "More details about the event",
                "date-of-event": "Date in YYYY-MM-DD format",
                "image": "image url of the link"
            },
        ]
    }
    res = make_response(jsonify(response_body), 200)
    return res


@app.route('/past')
def past():
    return get_events("past_events")


@app.route('/ongoing')
def ongoing():
    return get_events('ongoing_events')


@app.route('/upcoming')
def upcoming():
    return get_events('upcoming_events')


@app.route('/<event_time>/edit')
def edit(event_time):
    if(event_time == "past" or event_time == "ongoing" or event_time == "upcoming"):
        table_name = event_time + "_events"
        res = get_events(table_name, True)
        events = res['events']
        size = res['size']
        return render_template('editor.html', size=size, events=events, event_time=event_time.capitalize(), table_name=table_name)
    else:
        return "Wrong Parameter Supplied"


@app.route("/update", methods=['POST'])
def update():
    data = request.form.to_dict()
    if(data['password'] == PASSWORD):
        commands = get_commands(data, data['table_name'])

        cur = mysql.connection.cursor()

        for i in commands:
            try:
                print("Executing: " + i)
                cur.execute(i)
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                print(e)

        mysql.connection.commit()
        cur.close()

        return "Successfully Updated"
    else:
        return "Incorrect Password"


if __name__ == "__main__":
    if(env == 'dev'):
        app.run(debug=True)
    else:
        app.run()
