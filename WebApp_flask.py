from flask import Flask, render_template, flash, request, url_for, redirect
from content_management import Content
from dbconnect import connection

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


# if __name__ == "__main__":
#     app.run()
@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        c, conn = connection()
        return ("Okay")

    except Exception as e:
        return (str(e))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.debug = True
    app.run()
