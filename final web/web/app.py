from flask import Flask, render_template, redirect, session, request, url_for
from flask_oauthlib.client import OAuth
from functools import wraps


app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = '95eb7361f10fed70c01d22714974ca2c'


oauth = OAuth(app)

google = oauth.remote_app(
	'google',
	base_url='https://www.googleapis.com/oauth2/v1/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://accounts.google.com/o/oauth2/token',
	authorize_url='https://accounts.google.com/o/oauth2/auth',
	request_token_params={'scope': 'email'},
	consumer_key='51797849840-a1487e07e8715v3q49l9fd8bo71psafp.apps.googleusercontent.com',
	consumer_secret='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',
)

@google.tokengetter
def get_google_token():
	return session.get('google_token')


def login_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		if 'google_token' in session:
			return f(*args, **kwargs)
		return redirect("/login")
	return decorator


@app.route("/login/google")
def google_login():
	return google.authorize(callback=url_for('authorized', _external=True))

@app.route("/login/authorized")
def authorized():
	response = google.authorized_response()
	if response is None or response.get('access_token') is None:
		return "Access denied: reason={} error={}".format(
			request.args['error_reason'],
			request.args['error_description']
		)
	
	session['google_token'] = (response['access_token'], '')

	return redirect("/home")


@app.route("/scrollimage.html")
def index():
	return render_template("scrollimage.html")


@app.route("/login.html")
def login():
	return render_template("login.html")


@app.route("/logout")
def logout():
	session.clear()
	return redirect('/')


@app.route("/")
def ahoo():
	return redirect("/scrollimage.html")


@app.route("/home")
@login_required
def home():
	user_info = google.get('userinfo')
	return f"Hello, {user_info.data['email']}"


@app.route("/about.html")
def about():
	return render_template("about.html")


@app.route("/overview.html")
def overview():
	return render_template("overview.html")


@app.route("/ministry.html")
def ministry():
	return render_template("ministry.html")


@app.route("/introduction.html")
def introduction():
	return render_template("introduction.html")


@app.route("/yoga.html")
def yoga():
	return render_template("yoga.html")


@app.route("/ayurved.html")
def ayuved():
	return render_template("ayuved.html")


@app.route("/unani.html")
def unani():
	return render_template("unani.html")


@app.route("/siddha.html")
def siddha():
	return render_template("siddha.html")


@app.route("/homeopathy.html")
def homeopathy():
	return render_template("homeopathy.html")


@app.route("/gibbrish")
def gibbrish():
	return render_template("scrollimage.html")


if __name__ == "__main__":
	app.run(debug=True)