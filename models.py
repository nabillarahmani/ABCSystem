from abcmain import db
from sqlalchemy.sql import func
import datetime
import time


class Users(db.Model):
	"""
		Model for the users table
	"""

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	identification_number = db.Column(db.String(32))
	status_cekal = db.Column(db.Boolean)

	def __init__(self, identification_number, status_cekal):
		self.identification_number = identification_number
		self.status_cekal = status_cekal

	def __repr__(self):
		return '<id {}>'.format(self.id)


class Loggings(db.Model):
	"""
		Model for the loggings table
	"""
	__tablename__ = 'loggings'

	id = db.Column(db.Integer, primary_key = True)
	identification_number = db.Column(db.String(32))
	fullname = db.Column(db.String(64))
	photo_taken = db.Column(db.String(4096))
	status_verification_fingerprint = db.Column(db.Boolean)
	status_verification_cekal = db.Column(db.Boolean)
	timestamp_traveller = db.Column(db.TIMESTAMP(timezone=False))

	def __init__(self, identification_number, fullname, photo_taken, status_verification_cekal, status_verification_fingerprint, timestamp_traveller):
		self.identification_number = identification_number
		self.fullname = fullname
		self.photo_taken = photo_taken
		self.status_verification_cekal = status_verification_cekal
		self.status_verification_fingerprint = status_verification_fingerprint
		self.timestamp_traveller = timestamp_traveller


	def __repr__(self):
		return '<id {}>'.format(self.id)