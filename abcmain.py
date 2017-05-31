from flask import Flask
from flask import Response
from flask import redirect
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

env = DotEnv()
env.init_app(app)
db = SQLAlchemy()
db.init_app(app)

heroku = Heroku(app)

app.config.from_object(os.environ['APP_SETTINGS'])
# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'ifweirdnabey!2',
#     'db': 'abcsystem',
#     'host': 'localhost',
#     'port': '5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES



env.eval(keys={
	'DEBUG': bool,
	'TESTING': bool
})



@app.route("/logging", methods=['POST'])
def logging():
	import time
	import request
	"""
		This method will respectively log the data into database
	"""	
	try:
		data = request.get_data()
		return 'OK', 200
	except:
		return 'FAILED', 404
    

@app.route('/get_cekal/<identification_number>', methods=['GET'])
def get_cekal(identification_number):
	"""
	This routing will handle every get request
	"""
	pass
    

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