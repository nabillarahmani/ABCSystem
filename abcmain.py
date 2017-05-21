from flask import Flask
from flask import Response
from flask import redirect
from flask import render_template
from flask import render_template_string
from flask import request
from flask import session
from flask import stream_with_context
from flask import url_for
from flask_dotenv import DotEnv
from flask.ext.sqlalchemy import SQLAlchemy
from smartcard.System import readers
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
from binascii import unhexlify, b2a_base64
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db_cekal'
db = SQLAlchemy(app)
env = DotEnv()
env.init_app(app)
env.eval(keys={
	'DEBUG': bool,
	'TESTING': bool
})

# Create our database model
class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	identification_number = db.Column(db.String(120), unique=True)
	status_cekal = db.Column(db.Boolean())

	def __init__(self, identification_number, status_cekal):
		self.identification_number = identification_number
		self.status_cekal = status_cekal

	def __repr__(self):
		return '< %r>' % self.identification_number



@app.route("/logging", methods['POST'])
def logging():
	import time
	"""
		This method will respectively log the data into database
	"""


		
	# render_template('index.html', title='', current_page='ABC Gate Home')


@app.route('/get_cekal/<identification_number>', methods=['GET'])
def get_cekal(identification_number):
    """
    	This routing will handle every get request
    """


@app.route("/")
def open_gate():
	import RPi.GPIO as GPIO
	"""
		This method will switch the gate, so that the traveller can pass the gate
	"""
	# setting a current mode
	GPIO.setmode(GPIO.BCM)
	#removing the warings 
	GPIO.setwarnings(False)
	#creating a list (array) with the number of GPIO's that we use 
	pin = 18 
	#setting the mode for all pins so all will be switched on 
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,  GPIO.HIGH)
	#cleaning all GPIO's 
	GPIO.cleanup()
	return redirect_url(url_for('logging'))


@app.errorhandler(404)
def page_not_found_error(err):
	"""
	Render the view of error 404 page
	"""
	return render_template('404.html', title='Page not found', current_page='404')


@app.errorhandler(500)
def internal_server_error(err):
	"""
	Render the view of error 500 page
	"""
	return render_template('500.html', title='Server internal server error', current_page='500')


if __name__ == "__main__":
	app.secret_key = 'nyemnyemnyem'
	app.run(host=app.config['HOST'], port=int(app.config['PORT']))