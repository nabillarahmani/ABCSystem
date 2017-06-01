from abcmain import app, db
from models import Users
from models import Loggings
import datetime

global loggings
global users

def create_dummy_loggings():
	global loggings
	loggings = list()
	
	loggings.append(Loggings(idenfitication_number='1306381730', fullname='Andinta Zumar', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381731', fullname='Sumanadi Rahmanadhika', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381732', fullname='Rizky Noviandi', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381733', fullname='Emil Farisan', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381734', fullname='Farrah Hunafa', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381735', fullname='Tengku Huday', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381736', fullname='Nabilla Rahmani Zhafira', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381737', fullname='Ayu Saida', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381738', fullname='Faridah Nur Suci', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381739', fullname='Abidzar Gifari', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))
	loggings.append(Loggings(idenfitication_number='1306381730', fullname='Citra Glory', photo_taken='', 
							 status_verification_cekal=True, status_verification_fingerprint= True,
							 timestamp_traveller=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))


def create_dummy_users():
	global users
	users = list()

	users.append(Users(idenfitication_number='1306381730', status_cekal= False))
	users.append(Users(idenfitication_number='1306381731', status_cekal= False))
	users.append(Users(idenfitication_number='1306381732', status_cekal= False))
	users.append(Users(idenfitication_number='1306381733', status_cekal= False))
	users.append(Users(idenfitication_number='1306381734', status_cekal= False))
	users.append(Users(idenfitication_number='1306381735', status_cekal= False))
	users.append(Users(idenfitication_number='1306381736', status_cekal= False))
	users.append(Users(idenfitication_number='1306381737', status_cekal= False))
	users.append(Users(idenfitication_number='1306381738', status_cekal= False))
	users.append(Users(idenfitication_number='1306381739', status_cekal= False))
	users.append(Users(idenfitication_number='1306381740', status_cekal= False))
	users.append(Users(idenfitication_number='1306381741', status_cekal= True))
	users.append(Users(idenfitication_number='1306381742', status_cekal= True))
	users.append(Users(idenfitication_number='1306381743', status_cekal= True))
	users.append(Users(idenfitication_number='1306381744', status_cekal= True))
	users.append(Users(idenfitication_number='1306381745', status_cekal= True))
	users.append(Users(idenfitication_number='1306381746', status_cekal= True))
	users.append(Users(idenfitication_number='1306381747', status_cekal= True))
	

def create_dummy():
	global loggings
	global users
	# Do commit each loggings!
	try:
		for logging in loggings:
			db.add(logging)
			db.commit()
		for user in users:
			db.add(user)
			db.commit()
	except Exception as e:
		app.logger.debug(str(e))


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=int(app.config['PORT']))
    create_dummy()
