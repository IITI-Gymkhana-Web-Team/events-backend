from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL
import MySQLdb
import yaml
import os
from dbConfig import database_config

app = Flask(__name__)

env = ""

if env == "dev":
    dev = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
    DATABASE_URL  = dev['CLEARDB_DATABASE_URL']
    PASSWORD  = dev['PASSWORD']

else:
    DATABASE_URL  = os.environ.get('CLEARDB_DATABASE_URL')
    PASSWORD  = os.environ.get('PASSWORD')

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

def get_events(table_name):
    cur = mysql.connection.cursor()
    cur.execute('select * from ' + table_name + ';')
    events = cur.fetchall()  
    print(len(events))
    
    event_list = []
    for i in events:
        obj = {
            "title": i[0],
            "description": i[1],
            "details": i[2],
            "date-of-event": i[3],
            "image": i[4]
        }
        event_list.append(obj)
    response_body = {
    "size": len(events),
    "events": event_list
}
    res = make_response(jsonify(response_body), 200)
    return res

@app.route('/')
def example():
    response_body = {
    "size": 3,
    "events": [
        {
            "title": "This is an example",
            "description": "Example event",
            "details": "More details about the event",
            "date-of-event": "Date in YYYY-MM-DD format",
            "image": "image url of the link"
        },
        {
            "title": "TItle of event",
            "description": "Short description of the event",
            "details": "More details about the event",
            "date-of-event": "Date in YYYY-MM-DD format",
            "image": "image url of the link"
        },
        {
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
    return get_events("past_event")

@app.route('/ongoing')
def ongoing():
    return get_events('ongoing_events')

@app.route('/upcoming')
def upcoming():
    return get_events('upcoming_events')


if __name__ == "__main__":
    if(env == 'dev'):
        app.run(debug=True)
    else:
        app.run()