import json

import unittest

from flask import url_for

from app import db
from test.base import BaseTest
from app.models.database import User, Bucketlist, Bucket_items


class testBucketlistItems(BaseTest):

	def setUp(self):
		db.create_all()
		user = User(
			username='marvin',
			email='marvin@gmail.com',
			access_token='Authorization')
		user.hash_password('12345')
		bucket = Bucketlist(
			bucket_name='Python',
			bucket_id=1,4
			created_by=1
			)
		db.session.add(user)
		db.session.add(bucket)
		db.session.commit()

	def test_create_new_bucketlist_item(self):
		data = json.dumps({'item_name':'Flask framework', 'task_done':'False'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('createnewbucketitem', bucket_id=1), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertEqual(200, output['status_code'])
		self.assertIn('New Bucketlist item created', output['message'])

	def test_create_new_bucketlist_item_for_non_existing_bucket(self):
		data = json.dumps({'item_name':'Flask framework', 'task_done':'False'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(url_for('createnewbucketitem', bucket_id=10), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertEqual(404, output['status_code'])
		self.assertIn('Bucket doesn\'t exist', output['message'])	

	def test_create_new_bucketlist_with_no_data(self):
		data = json.dumps({})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.post(
			url_for('createnewbucketitem', bucket_id=1), data=data, headers=headers)
		self.assert_401(response)

	def test_edit_specific_bucket(self):
		data = json.dumps({'new_item_name':'Django Framework','task_done':'False'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(
			url_for('modifyspecificbucketlistitem', bucket_id=1, item_id=1), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assert_status(response, 200)
		
	def test_edit_specific_non_existing_bucketlist_item(self):
		data = json.dumps({'new_item_name':'Django Framework','task_done':'False'})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(
			url_for('modifyspecificbucketlistitem', bucket_id=1, item_id=10), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Bucket item doesn\'t exist', output['message'])

	def test_edit_specific_bucket_with_no_data(self):
		data = json.dumps({})
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.put(
			url_for('modifyspecificbucketlistitem', bucket_id=1, item_id=1), data=data, headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assert_status(response, 401)
		
	def test_delete_specific_non_existing_bucket_item(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.delete(
			url_for('modifyspecificbucketlistitem', bucket_id=1, item_id=10), headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assertIn('Bucket item doesn\'t exist', output['message'])
	
	def test_delete_specific_bucket_item(self):
		headers = {'Authorization': 'Authorization', 'content-type': 'application/json'}
		response = self.client.delete(
			url_for('modifyspecificbucketlistitem', bucket_id=1, item_id=1), headers=headers)
		output = json.loads(response.get_data(as_text=True))
		self.assert_status(response, 200)

	def tearDown(self):
		db.session.close_all()
		db.drop_all()


if __name__ == '__main__':
		unittest.main()			
