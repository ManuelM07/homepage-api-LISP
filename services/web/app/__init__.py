from flask import jsonify, request
from flask_login import LoginManager, login_user, current_user, logout_user
from app.model import app, User, db, Zone
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


# HTTP POST - LOGIN USER 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user != None:
            if check_password_hash(user.password, request.form.get("password")):
                if user.active:
                    user.is_authenticated = True
                    login_user(user)

                    return jsonify(response={"success": "The user has successfully login."})
                else:
                    return jsonify(response={"error": "The user doesn't have access."}), 404
            else:
               return jsonify(response={"error": "Password incorrect, please try again."}), 404
        else:
            return jsonify(response={"error": "That email does not exist, please try again."}), 404

 
# HTTP POST - CREATE USER 
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
                active=True,
                role="client",
                )
            db.session.add(user)
            db.session.commit()

            user.is_authenticated = True
            login_user(user)

            return jsonify(response={"success": "User has successfully register."}), 200 # specified http status
            
    return jsonify(response={"success": "The email is already registered, please log in or other email."})


# HTTP GET - LOGOUT CURRENT USER
@app.route('/logout')
def logout():
    user = current_user
    user.is_authenticated = False
    user.is_active = False
    print(user.is_active)
    logout_user()
    return jsonify(Response={"success": "user has successfully logged out."})


# HTTP PATCH - activate or inactivate user
@app.route("/status-user/<user_id>", methods=["GET", "PATCH"])
def status_user(user_id):
    user = User.query.get(user_id)
    if user != None:
        user.active = not user.active
        db.session.commit()
        return jsonify(response={"success": "Successfully updated user status."})
    else:
        return jsonify(error={"Not Found": "Sorry, a user with that id was not found in the database."})


# HTTP GET - get all users
@app.route("/all-users")
def all_users():
    users = User()
    all_users = [user_x.to_dict() for user_x in users.query.all()]
    return jsonify(users=all_users)


# HTTP GET - get all zones
@app.route("/all-zones")
def all_zones():
    zones = Zone()
    all_zones = [zone.to_dict() for zone in zones.query.all()]
    return jsonify(zones=all_zones)


# HTTP PATCH - update user
@app.route("/update-user/<user_id>", methods=["GET", "PATCH"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user != None:
        email = request.form.get("email")
        if email: user.email = email

        name = request.form.get("name")
        if name: user.name = name

        years = request.form.get("years")
        if years: user.years = years

        birthday = request.form.get("birthday")
        if birthday: user.birthday = birthday

        weight = request.form.get("weight")
        if weight: user.weight = weight

        height = request.form.get("height")
        if height: user.height = height

        db.session.commit()

        return jsonify(response={"success": "Successfully updated user data."})
    else:
        return jsonify(error={"Not Found": "Sorry, a user with that id was not found in the database."})


# HTTP GET - get current user
@app.route("/current-user", methods=["GET", "PATCH"])
def is_current_user():
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    return jsonify(response={"name": str(user.name)})