import os
import jwt
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context
from config import Config
 
from app import db
 
class User(db.Model):
	__tablename__ = 'user'
	# Here we define db.Columns for the table person
	# Notice that each db.Column is also a normal Python instance attribute.
	username = db.Column(db.String(250))
	email = db.Column(db.String(250))
	hashed_pass = db.Column(db.String(250))
	access_token = db.Column(db.String(250), default='None')
	user_id = db.Column(db.Integer, primary_key=True, unique=True)
	bucketlist = db.relationship('Bucketlist', backref='user', lazy="dynamic")

	# def __init__(self,username,email,hashed_pass=None,access_token=None,buck):
 #        self.id = id
 #        self.name = name
 #        self.addresses = addresses

	#Borrowed from "https://github.com/miguelgrinberg/REST-auth/blob/master/api.py"

	def hash_password(self, password):
		self.hashed_pass = pwd_context.encrypt(password)
	   
	def verify_password(self, password):
		return pwd_context.verify(password, self.hashed_pass)	

	def generate_access_token(self):
		self.access_token = jwt.encode(
			{'user_id': self.user_id},
			Config.SECRET_KEY,
			algorithm='HS256')
		return self.access_token

	def verify_access_token(self, access_token):
		return jwt.decode(access_token,"secret")	

class Bucketlist(db.Model):
	__tablename__ = 'bucketlist'

	bucket_name = db.Column(db.String(250), nullable=False)
	bucket_id = db.Column(db.Integer, primary_key=True, unique=False)
	date_created = db.Column(db.String(250))
	date_modified = db.Column(db.String(250))
	created_by = db.Column(db.Integer, ForeignKey('user.user_id'))
	items_list = db.relationship('Bucket_items', backref='bucketlist', lazy="dynamic")

	def __int__(bucket_name, date_created, created_by, date_modified, items_list=[]):
		self.bucket_name = bucket_name
		self.date_modified = date_modified
		self.created_by = created_by
		self.date_created = date_created
		self.items_list = items_list

	def __repr__(self):
		return 'Bucket( name: {} id: {} user id: {} items: {})'.format(
			self.bucket_name, self.bucket_id, self.created_by, self.items_list)

class Bucket_items(db.Model):
	__tablename__ = 'bucket_items'

	item_name = db.Column(db.String(250), nullable=False)
	item_id = db.Column(db.Integer, unique=True, primary_key=True)
	source_item_id = db.Column(db.Integer, db.ForeignKey('bucketlist.bucket_id'))
	date_created = db.Column(db.String(250))
	date_modified = db.Column(db.String(250))
	task_done = db.Column(db.String(250), default='False')
	
	def __init__(self, item_name, date_created, date_modified, task_done='False'):
		self.item_name = item_name
		self.date_modified = date_modified
		self.date_created = date_created
		self.task_done = task_done

	def __repr__(self): 
		return 'Bucket item( name: {} id: {} source id: {} task completed: {})'.format(
			self.item_name, self.item_id, self.source_item_id, self.task_done)

