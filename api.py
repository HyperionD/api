from flask import Flask, jsonify, request
from flask_cors import CORS

from note import models as note_model

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)


@app.before_request
def __db_connect():
    note_model.db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        note_model.db.close()


@app.route("/", methods=["GET"])
def hello():
    resp = jsonify({"hello": "world"})
    return resp


@app.route("/note_api/notes", methods=["GET"])
def note_get():
    note_title = request.args.get("note_title")
    return jsonify(note_model.get_note(note_title))