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


@app.route('/test')
def testing():
	import time
	import datetime
	import requests
	data_logging = {'identification_number': '13400400493', 'timestamp_traveller': '2017-06-02 13:35:10', 'status_cekal': False, 'full_name': '', 'photo_taken': '', 'fullname': 'PUTRI PARAHITA'}
	ts = time.time()
	ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	data_logging['timestamp_traveller'] = ts
	result = requests.post("http://localhost:8080/logging_data", params=data_logging)	
	return 'nyem'


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
	data = {}
	data['identification_number'] = request.args.get('identification_number')
	data['fullname'] = request.args.get('fullname')
	data['photo_taken'] = request.args.get('photo_taken')
	data['status_verification_cekal'] = request.args.get('status_verification_cekal')
	data['status_verification_fingerprint'] = request.args.get('status_verification_fingerprint')
	app.logger.debug(data)
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
			app.logger.debug(str(e))
			return 'ERROR ON QUERY', 204
	else:
		app.logger.debug('/logging_data data is not in dictionary!')
		return 'DATA MUST BE A DICTIONARY', 400


@app.route('/test_data')
def get_test_data():
	"""
	"""
	from models import Users
	from models import Loggings
	app.logger.debug("/test_data accessed")
	query_user = Users.query.all()
	query_logging = Loggings.query.all()
	result = ''
	for data in query_user:
		result += 'identification_number : {}, status_cekal : {}\n'.format(data.identification_number, data.status_cekal)
	result += 'DATA LOGGING : \n'
	for data in query_logging:
		result += 'identification_number : {} and photo_taken : {}\n'.format(data.identification_number, data.photo_taken)
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


@app.route('/empty_all_data')
def empty_table():
	from models import Users
	from models import Loggings

	# Get data for all users and drop the data
	try:
		users_row_deleted  = db.session.query(Users).delete()
		loggings_row_deleted = db.session.query(Loggings).delete()
		db.session.commit()
		app.logger.debug('successfully remove all data from tables')
		return 'users deleted : {}, loggings deleted : {}'.format(users_row_deleted, loggings_row_deleted)
	except Exception as e:
		app.logger.debug(str(e))
		return 'failed to destroy all data on tables'


def verification_cekal(identification_number):
	import requests
	"""
		This method will send a GET request into the API and retrieve cekal status
	"""
	result = False
	try:
		data = {'identification_number':identification_number}
		r = requests.get('http://webservice-abcsystem.herokuapp.com/get_cekal/', params=data)
		print(r.url)
		print(r.text)
		if r.status_code == 200:
			app.logger.debug('Succeed on getting status cekal')
		else:
			app.logger.debug('There is no data on this user')
		if r.text == 'False':
			result = False
		else:
			result = True
		return result 
	except:
		app.logger.debug('Failed on making request')
		return result	


# @app.route('/test_log_photo', methods=['POST'])
# def test_log_photo():
# 	import time
# 	import datetime
# 	# from io import BytesIO
# 	# from PIL import Image
# 	"""
# 		This method will respectively log the photo into 
# 		folder data
# 	"""
# 	app.logger.debug('Accessing test log photo for a large filter_by')
# 	baseurl = './data/'
# 	data = request.data
# 	try:
# 		ts = time.time()
# 		ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
# 		filename = ts + ''
# 		t = open(baseurl+ts+, "w+")
# 		t.write(data)
# 		t.close()
# 		app.logger.debug('successfully log a test data')
# 		return 'successfully log a test data'
# 	except Exception as e:
# 		app.logger.debug(str(e))
# 		return 'Failed test logging'


@app.route('/get_cekal/', methods=['GET'])
def get_cekal():
	from models import Users
	"""
	This routing will handle every get request
	"""
	data = request.args.get('identification_number')
	identification_number = data
	app.logger.debug("/get_cekal accessed")
	app.logger.debug("Get cekal for : {}".format(identification_number))
	try:
		user = Users.query.filter_by(identification_number=identification_number).first()
		# If there's no users in database, we indicate them as not cekal
		if user is None:
			app.logger.debug('No user in database cekal')
			return str(False), 200
		# If there's a user then return with the data
		else:
			status_cekal = user.status_cekal
			app.logger.debug('The user with no : {} is getting status : {}'.format(identification_number, status_cekal))
			return str(status_cekal), 200
	except Exception as e:
		app.logger.debug(str(e))
		return 'ERROR ON QUERY', 400


@app.route('/add_users/', methods=['POST'])
def add_users():
	"""
	"""
	from models import Users
	import ast
	data = request.data
	data = ast.literal_eval(data)
	identification_number = data['identification_number']
	status_cekal = data['status_cekal']
	user = Users(identification_number, status_cekal)
	try:
		db.session.add(user)
		db.session.commit()
		app.logger.debug("Successfully commit a new user into database")
		return "successfully commit a new user into database"
	except Exception as e:
		app.logger.debug("Failed to commit a new user")
		return "failed to commit a new user"


@app.route('/')
def index():
	return 'welcome to abc webservice!'


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
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381731', fullname='Sumanadi Rahmanadhika', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381732', fullname='Rizky Noviandi', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381733', fullname='Emil Farisan', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381734', fullname='Farrah Hunafa', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381735', fullname='Tengku Huday', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381736', fullname='Nabilla Rahmani Zhafira', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381737', fullname='Ayu Saida', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381738', fullname='Faridah Nur Suci', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381739', fullname='Abidzar Gifari', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(identification_number='1306381740', fullname='Citra Glory', photo_taken='', 
							 status_verification_cekal=False, status_verification_fingerprint= True,
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