from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from wtforms import Form,BooleanField,TextField, PasswordField, validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from dbconnect import connection
import gc

TOPIC_DICT = Content()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/dashboard/')
def dashboard():
    # flash("Flashing")
    return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_found(e):
    return render_template('405.html')


# @app.route('/slashboard/')
# def slashboard():
#     try:
#         return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT)
#     except Exception as e:
#         return render_template("500.html", error=e)


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid credentials. Try again."
        return render_template("login.html")
    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error)


class RegistrationForm(Form):
    username = TextField('Username', [validators.length(min=4, max=20)])
    email = TextField('Email Address', [validators.length(min=4, max=50)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('Confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the terms of service and the privacy notice'.[validators.Required()])


# if __name__ == "__main__":
#     app.run()
@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        # c, conn = connection()
        # return ("Okay")
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()
            x = c.execute("SELECT * FROM users WHERE username =(%s)", (thwart(username)))

            if int(len(x)) > 0:
                flash("That name is already chosen, please choose another")
                return render_template('register.html', form=form)
            else:
                c.execute("INSERT INTO users (username, password, email,tracking) VALUE (%s,%s,%s,%s)",
                          (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-programming/")))
            conn.commit()
            flash("Thanks for registering!")
            c.close()
            conn.close()

            gc.collect()
            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)

    except Exception as e:
        return (str(e))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.debug = True
    app.run()
