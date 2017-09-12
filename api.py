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
    if not note_model.db.is_closed():
        note_model.db.close()


@app.route("/", methods=["GET"])
def hello():
    resp = jsonify({"hello": "world"})
    return resp


@app.route("/api/note/notes", methods=["GET"])
def note_get():
    note_title = request.args.get("note_title")
    return jsonify(note_model.get_note(note_title))


@app.route("/api/note/notes", methods=["POST"])
def note_post():
    post_data = request.json
    return_msg = note_model.save_note(post_data)
    resp_data = {"status": return_msg}
    return jsonify(resp_data)


@app.route("/api/note/notes", methods=["PUT"])
def note_put():
    put_data = request.json
    return_msg = note_model.update_note(put_data)
    resp_data = {"status": return_msg}
    return jsonify(resp_data)


@app.route("/api/note/notes", methods=["DELETE"])
def note_delete():
    note_title = request.args.get("note_title")
    return_msg = note_model.delete_note(note_title)
    resp_data = {"status": return_msg}
    return jsonify(resp_data)


@app.route("/api/note/labels", methods=["GET"])
def labels_get():
    note_title = request.args.get("note_title")
    if note_title is None:
        return jsonify(note_model.get_all_labels())
    else:
        return jsonify(note_model.get_labels(note_title))


@app.route("/api/note/labels", methods=["POST"])
def labels_post():
    post_data = request.json
    return_msg = note_model.save_label(post_data)
    resp_data = {"status": return_msg}
    return jsonify(resp_data)


@app.route("/api/note/labels", methods=["DELETE"])
def labels_delete():
    label_name = request.args.get("label_name")
    return_msg = note_model.delete_label(label_name)
    resp_data = {"status": return_msg}
    return jsonify(resp_data)


@app.route("/api/note/menus", methods=["GET"])
def menus_get():
    return jsonify(note_model.get_menu())

