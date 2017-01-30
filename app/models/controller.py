import re

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from app import db
from passlib.apps import custom_app_context as pwd_context

 
from app.models.database import User, Bucketlist, Bucket_items



def update_access_token(access_token, user_id):
	query = db.session.query(User).filter_by(user_id=user_id).first()
	query.access_token = access_token
	db.session.commit()

def check_new_user_credentials(username, email):

	try:
		query = db.session.query(User).filter_by(email=email).first()
		if query:
			return False
		else:
			return True
	except Exception as e:
		return False

def save_new_user(user):
	db.session.add(user)
	db.session.commit()

def get_all_bucketlists(user_id, limit=20, start_value=0, search=None, main_url='http:127.0.0.1:5000/api/v1'):
	query = db.session.query(Bucketlist).filter_by(created_by=user_id).all()
	no_of_buckets = len(query)

	query = db.session.query(Bucketlist).filter_by(created_by=user_id).slice(start_value,limit+start_value).all()
	search_string = get_searched_data(query,"String")
	search_list = re.findall(r'\b[\w]*{}[\w]*'.format(search),search_string)
	

	if limit > 100:
		return [{"message":"excessive requested amount"}]
	elif len(search_list) > 0:
		this_bucket = []
		set_pagination(this_bucket, start_value, limit, no_of_buckets, main_url)	
	
		for bucket in query:
			if no_of_buckets != 0 and limit != 0 and bucket.bucket_name in search_list:
				all_buckets = {}
				all_buckets['bucket_name'] = bucket.bucket_name
				all_buckets['bucket_id'] = bucket.bucket_id
				all_buckets['bucket_owner_id'] = bucket.created_by
				all_buckets['bucket_items'] = get_bucketlist_items(bucket.bucket_id)

								
				this_bucket.append(all_buckets)
							
				no_of_buckets-=1
				limit-=1
			else:
				continue	
	else:
		this_bucket = []
		set_pagination(this_bucket, start_value, limit, no_of_buckets, main_url)	
		for bucket in query:
			if (no_of_buckets != 0 and limit != 0):
				all_buckets = {}
				all_buckets['bucket_name'] = bucket.bucket_name
				all_buckets['bucket_id'] = bucket.bucket_id
				all_buckets['bucket_owner_id'] = bucket.created_by
				all_buckets['bucket_items'] = get_bucketlist_items(bucket.bucket_id)
								
				this_bucket.append(all_buckets)
							
				no_of_buckets-=1
				limit-=1
			else:
				break	



	return this_bucket

def set_pagination(bucket, start, limit, bucket_size, main_url):
	
	if start+limit < bucket_size:
		bucket.append({"next":"{}/bucketlists?start={}&limit={}".format(main_url, start+limit, limit)})
	else:
		bucket.append({"next":"{}/bucketlists?start={}&limit={}".format(main_url, 0, limit)})	

	if start-limit > 0:
		bucket.append({"back":"{}/bucketlists?start={}&limit={}".format(main_url, start-limit, limit)})
	else:
		bucket.append({"back":"{}/bucketlists?start={}&limit={}".format(main_url, 0, limit)})

def get_searched_data(query, format_passed=None):
	list_data = []
	for bucket in query:
		list_data.append(bucket.bucket_name)

	if format_passed == "String":
		val = ','.join([str(item) for item in list_data])
		return val
	else:
		return list_data		

def get_bucketlist(user_id, bucket_id):
	query = db.session.query(Bucketlist).filter_by(created_by=user_id, bucket_id=bucket_id).first()

	this_bucket = []
	all_buckets = {}
	
	all_buckets['bucket_name'] = query.bucket_name
	all_buckets['bucket_id'] = query.bucket_id
	all_buckets['bucket_owner_id'] = query.created_by
	all_buckets['created_on'] = query.date_created
	all_buckets['last_modified'] = query.date_modified

	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id).all()
	
	this_bucket_item = []
	for items in query:
		all_bucket_items = {}
		all_bucket_items['item_id'] = items.item_id
		all_bucket_items['item_name'] = items.item_name
		all_bucket_items['task_done'] = items.task_done
		all_buckets['created_on'] = items.date_created
		all_buckets['last_modified'] = items.date_modified

		this_bucket_item.append(all_bucket_items)

	all_buckets['bucket_items'] = this_bucket_item
	

	this_bucket.append(all_buckets)

	return this_bucket	

def get_bucketlist_items(bucket_id):
	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id)
	this_bucket_item = []
	for items in query:
		all_bucket_items = {}
		all_bucket_items['item_id'] = items.item_id
		all_bucket_items['item_name'] = items.item_name
		all_bucket_items['task_done'] = items.task_done
		all_bucket_items['created_on'] = items.date_created
		all_bucket_items['last_modified'] = items.date_modified

		this_bucket_item.append(all_bucket_items)

	return this_bucket_item	

def get_specific_bucket_item(bucket_id, item_id):
	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id, item_id=item_id).first()
	return query

def delete_bucketlist(user_id, bucket_id):
	query = db.session.query(Bucketlist).filter_by(created_by=user_id, bucket_id=bucket_id)
	query.delete()
	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id)
	query.delete()

	db.session.commit()
	return get_all_bucketlists(user_id)

def edit_bucket_item(user_id, bucket_id, item_id, new_name, task_done, modified_time):
	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id, item_id=item_id).first()
	query.item_name = new_name
	query.date_modified = modified_time
	query.task_done = task_done
	db.session.commit()

	return get_bucketlist(user_id, bucket_id)

def edit_bucketlist(user_id, bucket_id,new_name, modified_time):
	query = db.session.query(Bucketlist).filter_by(created_by=user_id, bucket_id=bucket_id).first()
	query.bucket_name = new_name
	query.date_modified = modified_time
	db.session.commit()

	return get_bucketlist(user_id, bucket_id)	

def delete_bucket_list_item(user_id, bucket_id, item_id):
	query = db.session.query(Bucket_items).filter_by(source_item_id=bucket_id, item_id=item_id)
	query.delete()
	db.session.commit()

	return get_bucketlist(user_id, bucket_id)	
	
def get_user_name(user_id):
	query = db.session.query(User).filter_by(user_id=user_id).first()
	return query.username

def get_user_id(access_token):
	query = db.session.query(User).filter_by(access_token=access_token).first()
	value = query.user_id
	return value	

def save_new_bucketlist(bucketlist, access_token):
	user = db.session.query(User).filter_by(access_token=access_token).first()
	user.bucketlist.append(bucketlist)
	db.session.add(bucketlist)
	db.session.commit()

def save_new_bucketlist_item(bucketlist, user_id, bucket_id):
	bucket = db.session.query(Bucketlist).filter_by(created_by=user_id, bucket_id=bucket_id).first()
	bucket.items_list.append(bucketlist)
	db.session.add(bucketlist)
	db.session.commit()	

def hash_password(password):
	return pwd_context.encrypt(password)

def verify_password(password, username):
	value = db.session.query(User).filter_by(username=username).first()
	return pwd_context.verify(password, value.hashed_pass)	


def verify_user_credentials(username, password):
	current_user = db.session.query(User).filter_by(username=username).first()
	if current_user:
		value = verify_password(password, username)
	else:
		return {
			"message":"login failed",
			"status_code":403
			}

	if value == True:
		return {
			"message":"login successful",
			"status_code":200, 
			"user":current_user
			}
	else:
		return {
			"message":"login failed",
			"status_code":403
			}	
	

