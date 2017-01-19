import os
import jwt
from sqlalchemy import Column, ForeignKey, Integer, String

from passlib.apps import custom_app_context as pwd_context
 
from app import db
 
class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    username = Column(String(250))
    email = Column(String(250))
    hashed_pass = Column(String(250))
    access_token = Column(String(250), default='None')
    user_id = Column(Integer, primary_key=True, unique=True)
    bucketlist = relationship('Bucketlist', backref='user')


    #Borrowed from "https://github.com/miguelgrinberg/REST-auth/blob/master/api.py"

    def hash_password(self, password):
        self.hashed_pass = pwd_context.encrypt(password)
       
    def verify_password(self, password):
    	return pwd_context.verify(password, self.hashed_pass)	

    def generate_access_token(self):
    	self.access_token = jwt.encode(
	    	{'user_id': self.user_id},
	   		"secret",
	   		algorithm='HS256')
    	return self.access_token

    def verify_access_token(self, access_token):
    	return jwt.decode(access_token,"secret")	

class Bucketlist(db.Model):
	__tablename__ = 'bucketlist'

	bucket_name = Column(String(250), nullable=False)
	bucket_id = Column(Integer, primary_key=True, unique=False)
	items_list = relationship('Bucket_items', backref='bucketlist')
	date_created = Column(String(250))
	date_modified = Column(String(250))
	created_by = Column(Integer, ForeignKey('user.user_id')) 



class Bucket_items(db.Model):
	__tablename__ = 'bucket_items'

	item_name = Column(String(250))
	item_id = Column(Integer, unique=True, primary_key=True)
	source_item_id = Column(Integer, ForeignKey('bucketlist.bucket_id'))
	date_created = Column(String(250))
	date_modified = Column(String(250))
	task_done = Column(String(250), default='False')


