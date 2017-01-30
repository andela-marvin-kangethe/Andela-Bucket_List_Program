import json

import unittest

from flask import url_for

from app import db
from test.base import BaseTest
from app.models.database import User


class testBucketlist(BaseTest):

	def setUp(self):
		db.create_all()
		user = User(
			username='marvin',
			email='marvin@gmail.com',
			access_token='Authorization')
		user.hash_password('12345')
		db.session.add(user)
		db.session.commit()

	def test_view_all_buckets(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.get(url_for('viewallbucketlist'), headers=headers)
		self.assert_status(response, 200)

	def test_create_new_bucketlist(self):
		data = json.dumps({'bucket_name':'Python'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('viewallbucketlist'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertEqual(200, output['status_code'])
		self.assertIn('New Bucketlist created', output['message'])

	def test_create_new_bucketlist_with_no_data(self):
		data = json.dumps({})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('viewallbucketlist'), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('No bucketlist data passed', output['message'])

	def test_view_specific_bucket(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.get(url_for('modifyspecificbucketlist', bucket_id=1), headers=headers)
		self.assert_status(response, 200)
	
	def test_view_specific_non_existing_bucket(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.get(url_for('modifyspecificbucketlist', bucket_id=10), headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Bucket doesn\'t exist', output['message'])
	
	def test_edit_specific_bucket(self):
		data = json.dumps({'new_bucket_name':'Google GO'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(url_for('modifyspecificbucketlist', bucket_id=1), data=data, headers=headers)
		self.assert_status(response, 200)
	
	def test_edit_specific_non_existing_bucket(self):
		data = json.dumps({'new_bucket_name':'Google GO'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(url_for('modifyspecificbucketlist', bucket_id=10), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Bucket doesn\'t exist', output['message'])

	def test_edit_specific_bucket_with_no_new_data(self):
		data = json.dumps({})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(url_for('modifyspecificbucketlist', bucket_id=10), data=data, headers=headers)
		self.assert_401(response)
	
	def test_delete_specific_non_existing_bucket(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.delete(url_for('modifyspecificbucketlist', bucket_id=10), headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Bucket doesn\'t exist', output['message'])

	def tearDown(self):
		db.session.close_all()
		db.drop_all()

if __name__ == '__main__':
		unittest.main()			

   