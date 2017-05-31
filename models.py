from abcmain import app, db
from sqlalchemy.sql import func
import datetime
import time


class BaseModel(db.Model):
	"""
	Base data model for all objects
	"""
	__abstract__ = True

	def __init__(self, *args):
	    super().__init__(*args)

	def __repr__(self):
	    """Define a base way to print models"""
	    return '%s(%s)' % (self.__class__.__name__, {
	        column: value
	        for column, value in self._to_dict().items()
	    })

	def json(self):
	    """
	            Define a base way to jsonify models, dealing with datetime objects
	    """
	    return {
	        column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
	        for column, value in self._to_dict().items()
	    }


class Users(BaseModel, db.Model):
	"""
		Model for the users table
	"""

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	identification_number = db.Column(db.String(32))
	status_cekal = db.Column(db.Boolean)


class Loggings(BaseModel, db.Model):
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