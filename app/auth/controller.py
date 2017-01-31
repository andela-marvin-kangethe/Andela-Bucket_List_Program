import json
import re
from flask_restful import Resource, Api, abort
from flask import jsonify, request

from app.models.controller import *
from app.models.database import User
from app.validator.validate import (
	validate_password_length,
	validate_username_format,
	validate_email_format,
	validate_parameter_is_digit
	)


class Login(Resource):


	def get(self):
		return jsonify({"message": "Welcome to the BucketList API."
                        " Register a new user by sending a"
                        " POST request to /auth/register."
                        "Login by sending a POST request to"
						" /auth/login to get started."})

	def post(self):
		data = json.loads(request.get_data(as_text=True))
		if data:
			try:
				username = data['username']
				password = data['password']
			except Exception as e:
				abort(401, message='No username or password credentials passed')
			

			user_access = verify_user_credentials(username, password)
			if user_access['status_code'] == 200:
				
				Authorization = user_access['user'].generate_access_token()
				
				update_access_token(Authorization, user_access['user'].user_id)
					
				return jsonify({
					'message':'login successful',
					'status_code':200,
					'Authorization':Authorization
					})
					
			else:
				abort(403, message='Invalid user credentials provided.')	
			
		else:
			return jsonify({
						'message':'login failure',
						'status_code':404
						})


class Register(Resource):

	def get(self):
		return jsonify({"message": "Welcome to the BucketList API."
                        " Register a new user by sending a"
                        " POST request to /auth/register."
                        "Login by sending a POST request to"
						" /auth/login to get started."})

	def post(self):
		data = json.loads(request.get_data(as_text=True))

		if data:
			try:
				username = data['username']
				password = data['password']
				email = data['email']
			except Exception as e:
				abort(401, message='Registration credentials not found.')
			
			if validate_username_format(username) and \
				validate_password_length(password) and \
				validate_email_format(email):

				if check_new_user_credentials(username, email):

					user = User(username=username, email=email, access_token='None')
					user.hash_password(password)
					save_new_user(user)
					
					access_token = user.generate_access_token()
					update_access_token(access_token,user.user_id)

					return jsonify({
						'message':'Registration successfull',
						'Authorization':access_token
						})

					
				else:
					abort(403, message='User already exists.')	
				
			else:
				return jsonify({
					'message':'Invalid credentials format passed',
					'status_code':403
					})	


		else:
			abort(401, message='No credentials passed.')
				
