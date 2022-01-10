from flask import Flask, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import generate_password_hash, check_password_hash
import os
from functools import wraps
from distinct_types import *

app = Flask(__name__, static_folder='templates/static/dist', static_url_path='', template_folder='templates/static/dist')
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", default=str(os.urandom(24)))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db.session().expire_on_commit = False

auth = HTTPBasicAuth()


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if app.config["DEBUG"]:
            return fn()
        return auth.login_required(fn)()
    return wrapper


@app.route('/')
def public_table() -> WebTemplate:
    return render_template("public.html")


@app.route("/book_slot/free", methods=["GET"])
def show_free_slot() -> Tuple[JsonList, int]:
    from work_with_slots import get_free_slots
    result = get_free_slots()

    return json.dumps(result[0]), result[1]


@app.route("/book_slot", methods=["POST"])
def book_free_slot() -> Tuple[str, int]:
    from work_with_slots import book_slot

    return book_slot(request.json)


@app.route("/admin")
@login_required
def admin_table() -> WebTemplate:
    return render_template("admin.html")


@app.route("/admin/create_slots", methods=["POST"])
@login_required
def create_free_slots() -> Tuple[str, int]:
    from work_with_slots import add_slot

    return add_slot(request.json)


@app.route("/admin/get_slots", methods=["GET"])
@login_required
def get_slots() -> Tuple[JsonList, int]:
    from work_with_slots import get_slots

    result = get_slots()

    return json.dumps(result[0]), result[1]


@app.route("/admin/clear_slot", methods=["POST"])
@login_required
def clear_slot() -> Tuple[str, int]:
    from work_with_slots import clear_slot

    return clear_slot(request.json["id"])


@app.route("/admin/delete_slot", methods=["POST"])
@login_required
def delete_slot() -> Tuple[str, int]:
    from work_with_slots import delete_slot

    return delete_slot(request.json["id"])


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    users = {os.getenv("FLASK_ADMIN_USERNAME", default="put_your_username_here"): generate_password_hash(os.getenv("FLASK_ADMIN_PASSWORD", default="put_your_password_here"))}

    if username in users:
        return check_password_hash(users.get(username), password)

    return False


if __name__ == '__main__':
    app.run(debug=True)
