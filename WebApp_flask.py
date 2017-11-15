from flask import Flask, render_template, flash
from content_management import Content

TOPIC_DICT = Content()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/dashboard/')
def dashboard():
    flash("Flashing")
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
    return render_template("login.html")


# if __name__ == "__main__":
#     app.run()


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.debug = True
    app.run()
