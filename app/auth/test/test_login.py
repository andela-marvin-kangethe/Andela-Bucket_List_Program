import json

import unittest

from flask import url_for

from app import db
from run import api
from test.base import BaseTest
from app.models.database import User


class testLogin(BaseTest):

	def setUp(self):
		db.create_all()
		user = User(
			username='marvin',
			email='marvin@gmail.com',
			access_token='Authorization')
		user.hash_password('12345')
		db.session.add(user)
		db.session.commit()

	def test_user_login(self):
		data = json.dumps({"username":"marvin", "password":"12345"})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('login'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('login successful', output['message'])
		self.assert_status(response, 200)

	def test_unregistered_user_login(self):
		data = json.dumps({"username":"john", "password":"12345"})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('login'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Invalid user credentials provided', output['message'])

	def test_missing_login_credentials(self):
		data = json.dumps({"username":"marvin"})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('login'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('No username or password credentials passed', output['message'])


	def tearDown(self):
		db.session.close_all()
		db.drop_all()	    

if __name__ == '__main__':
		unittest.main()