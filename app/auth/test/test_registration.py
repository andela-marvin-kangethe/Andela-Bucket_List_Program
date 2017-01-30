import json

import unittest

from flask import url_for

from app import db
from test.base import BaseTest

from app.models.database import User

class testRegistration(BaseTest):

	def setUp(self):
		db.create_all()
		user = User(
			username='marvin',
			email='marvin@gmail.com',
			access_token='Authorization')
		user.hash_password('12345')
		db.session.add(user)
		db.session.commit()
		
	def test_user_can_register(self):
		data = json.dumps({"username":"john", "password":"12345", "email":"john@andela.com"})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('register'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assert_status(response, 200)
		self.assertIn('Registration successfull', output['message'])

	def test_user_cannot_register_with_invalid_credentials(self):
		data = json.dumps({'username':'1', 'password':'12345', 'email':'veiruc'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('register'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertEqual(403, output['status_code'])
		self.assertIn('Invalid credentials passed', output['message'])

	def test_user_already_exist(self):
		data = json.dumps({'username':'andrew','password':'123ded', 'email':'marvin@gmail.com'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('register'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('User already exists', output['message'])
		self.assert_status(response, 403)

	def tearDown(self):
		db.session.close_all()
		db.drop_all()	    
	

if __name__ == '__main__':
		unittest.main()			
	