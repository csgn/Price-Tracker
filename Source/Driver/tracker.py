import json
from database.database_connection import DatabaseConnection
from webdriver.webdriver_connection import WebDriverConnection

import settings
import handler

from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    while not WebDriverConnection.status:
        wconn = WebDriverConnection()

    while not DatabaseConnection.status:
        dconn = DatabaseConnection(settings.DATABASE_TABLES)

    handler.Scheduler.run(handler.Handler.refresh)
    handler.Cache.resetAll()

    return ":)", 404


@app.route('/refresh', methods=['POST'])
@cross_origin()
def refresh():
    code, msg = handler.Handler.refresh()

    if code in [400, 500]:
        msg = {'error': msg}

    return json.dumps(msg), code


@app.route('/track', methods=['POST'])
@cross_origin()
def track():
    code, msg = handler.Handler.track(request.json)

    if code in [400, 500]:
        msg = {'error': msg}

    return json.dumps(msg), code


if __name__ == '__main__':
    app.run()
