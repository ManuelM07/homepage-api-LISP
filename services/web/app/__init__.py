from flask import jsonify, request, abort, Response
from flask_login import LoginManager, login_user, current_user, logout_user
from app.model import app, User, db
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv
import os


load_dotenv()
login_manager = LoginManager()

app.config.from_object("app.config.Config")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_WERKZEUG")
login_manager.init_app(app)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def hello_world():
    return jsonify(hello="Api LISP")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':    
        user = User.query.filter_by(email=request.form.get("email")).first()

        if user == None:
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            user = User(
                name=request.form.get("name"), 
                email=request.form.get("email"), 
                password=password,
                dni=request.form.get("dni"),
                role="client",
                )
            db.session.add(user)
            db.session.commit()

            user.is_authenticated = True
            login_user(user)

            return jsonify(response={"success": "user has successfully register"}), 200 # specified http status
            
    return jsonify(response={"success": "The email is already registered, please log in or other email"})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)