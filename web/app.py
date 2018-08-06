from flask import \
    Flask, \
    flash, \
    redirect, \
    render_template, \
    request, \
    session, \
    url_for
from flask_bcrypt import Bcrypt
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import \
    scoped_session, \
    sessionmaker
import os
import requests

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_url = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        db=os.getenv("DB_NAME")
    )

# Set up database
engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

# bcrypt for hashing
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

# Auth Related Routes
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        if password == password_confirm:
            hashed_password = bcrypt.generate_password_hash(password)
            try:
                db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": email, "password": hashed_password})
                db.commit()
            except:
                flash('There was a problem with your registration, please try a new email address', 'error_message')
                return redirect(url_for('register'))
            session['user_email'] = email

            flash('Account Created Successfully', 'success_message')
            return redirect(url_for('home'))
        else:
            flash('Passwords did not match', 'error_message')
            return redirect(url_for('register'))

    return render_template("auth/register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE email=:email", {"email": email}).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['user_email'] = email

                flash('Login Successful', 'success_message')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password', 'error_message')
                return redirect(url_for('login'))
        else:
            flash('User Not found', 'error_message')
            return redirect(url_for('login'))

    return render_template("auth/login.html")


@app.route('/logout', methods=["POST"])
def logout():
    session['user_email'] = None

    flash('Logout Successful', 'success_message')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')