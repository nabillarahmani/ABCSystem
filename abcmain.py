from flask import Flask
from flask import Response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import stream_with_context
from flask import url_for
from flask_dotenv import DotEnv
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import time
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy()
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
app.logger.setLevel(app.config['LOG_LEVEL'])


@app.route("/logging_data", methods=['POST'])
def logging_data():
	import time
	from models import Loggings
	import ast
	"""
		This method will respectively log the data into database
	"""	
	app.logger.debug('/logging_data route accessed!')
	# Do parse the request data!
	data = request.data
	data = ast.literal_eval(data)
	if isinstance(data, dict):
		identification_number = ''
		fullname = ''
		photo_taken = ''
		status_verification_cekal = False
		status_verification_fingerprint = False
		timestamp_traveller = ''
		if 'identification_number' in data:	
			identification_number = data['identification_number']
		if 'fullname' in data:	
			fullname = data['fullname']
		if 'photo_taken' in data:	
			photo_taken = data['photo_taken']
		if 'status_verification_cekal' in data:	
			status_verification_cekal = data['status_verification_cekal']
		if 'status_verification_fingerprint' in data:	
			status_verification_fingerprint = data['status_verification_fingerprint']
		if 'timestamp_traveller' in data:	
			timestamp_traveller = data['timestamp_traveller']
		try:
			query = Loggings(identification_number, fullname, photo_taken, status_verification_cekal, status_verification_fingerprint, timestamp_traveller)
			db.session.add(query)
			db.session.commit()
			app.logger.debug('/logging_data succeed!')
			return 'SUCCEED QUERY', 200
		except Exception as e:
			app.logger.debug('/logging_data route failed on query!')
			return 'ERROR ON QUERY', 204
	else:
		app.logger.debug('/logging_data data is not in dictionary!')
		return 'DATA MUST BE A DICTIONARY', 400


@app.route('/test_data')
def get_test_data():
	from models import Users
	from models import Loggings

	query_user = Users.query.all()
	query_logging = Loggings.query.all()
	result = ''
	for data in query_user:
		result += 'identification_number : {}, status_cekal : {}\m'.format(data.identification_number, data.status_cekal)
	result += 'DATA LOGGING : \n'
	for data in query_logging:
		result += 'identification_number : {}\n'.format(data.identification_number)
	return result
	

@app.route('/create_dummy')
def create_dummy():
	loggings = create_dummy_loggings()
	users = create_dummy_users()
	# Do commit each loggings!
	app.logger.debug(loggings)
	try:
		for logging in loggings:
			db.session.add(logging)
			db.session.commit()
		for user in users:
			db.session.add(user)
			db.session.commit()
		return 'SUCCEED COMMIT DATA INTO DB'
		app.logger.debug('SUCCEED COMMIT DATA INTO DB')
	except Exception as e:
		app.logger.debug(str(e))
		return 'FAILED THERE IS AN ERROR'


@app.route('/get_cekal/<identification_number>', methods=['GET'])
def get_cekal(identification_number):
	from models import Users
	"""
	This routing will handle every get request
	"""
	try:
		user = Users.query.filter_by(identification_number=identification_number).first()
		print(user)
		if user is None:
			return 'NO USER', 204
		else:
			return user.status_cekal, 200
	except:
		return 'ERROR ON QUERY', 204


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


def create_dummy_loggings():
	from models import Loggings
	import datetime

	loggings = []
	ts = time.time()
	
	loggings.append(Loggings(identification_number='1306381730', fullname='Andinta Zumar', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381731', fullname='Sumanadi Rahmanadhika', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381732', fullname='Rizky Noviandi', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381733', fullname='Emil Farisan', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381734', fullname='Farrah Hunafa', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381735', fullname='Tengku Huday', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381736', fullname='Nabilla Rahmani Zhafira', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381737', fullname='Ayu Saida', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381738', fullname='Faridah Nur Suci', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381739', fullname='Abidzar Gifari', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381730', fullname='Citra Glory', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	return loggings


def create_dummy_users():
	from models import Users
	users = []

	users.append(Users(identification_number='1306381730', status_cekal= False))
	users.append(Users(identification_number='1306381731', status_cekal= False))
	users.append(Users(identification_number='1306381732', status_cekal= False))
	users.append(Users(identification_number='1306381733', status_cekal= False))
	users.append(Users(identification_number='1306381734', status_cekal= False))
	users.append(Users(identification_number='1306381735', status_cekal= False))
	users.append(Users(identification_number='1306381736', status_cekal= False))
	users.append(Users(identification_number='1306381737', status_cekal= False))
	users.append(Users(identification_number='1306381738', status_cekal= False))
	users.append(Users(identification_number='1306381739', status_cekal= False))
	users.append(Users(identification_number='1306381740', status_cekal= False))
	users.append(Users(identification_number='1306381741', status_cekal= True))
	users.append(Users(identification_number='1306381742', status_cekal= True))
	users.append(Users(identification_number='1306381743', status_cekal= True))
	users.append(Users(identification_number='1306381744', status_cekal= True))
	users.append(Users(identification_number='1306381745', status_cekal= True))
	users.append(Users(identification_number='1306381746', status_cekal= True))
	users.append(Users(identification_number='1306381747', status_cekal= True))
	return users

if __name__ == "__main__":
	app.secret_key = 'nyemnyemnyem'
	app.run(host=app.config['HOST'], port=int(app.config['PORT']))