import re

def validate_password_length(password):
	if len(password) > 4:
		return True
	else:
		return False

def validate_username_format(username):
	#Search if the name has an numeric number
	if len(re.findall(r'\d+',username)) > 0:
		return False
	else:
		return True	

def validate_email_format(email):
	if len(re.findall(r'\b[\w]*{}[\w]*{}[\w]*'.format('@','.'),email)) < 1:
		return False
	else:
		return True	

def validate_parameter_is_digit(number):
	try:
		if number.isdigit():
			return True
		else:
			return False	
	except Exception as e:
		raise False