import json
import datetime
from flask_restful import Resource, abort
from flask import jsonify, request
from app.models.controller import *
from app.models.database import User, Bucketlist, Bucket_items
from app.validator.validate import (
    validate_password_length,
    validate_username_format,
    validate_email_format,
    validate_parameter_is_digit
    )
from config import Config



class BucketList(Resource):
    
    def get(self):
        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception:
            abort(401, message='Access forbidden, Login to continue.')

        start_point = request.args.get('start') or 0
        limit_size = request.args.get('limit') or 20
        search_value = request.args.get('q') or None
        base_root = "{}{}".format(request.url_root.decode('utf-8'), Config.API_ROOT)

        all_buckets = get_all_bucketlists(
                get_user_id(request.headers.get('Authorization')),
                int(limit_size),
                int(start_point),
                search_value,
                base_root
            )
        
        return jsonify({'bucketlists':all_buckets})
        
    def post(self):
        try:
            get_user_id(request.headers.get('Authorization'))
            
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        data = json.loads(request.get_data())
        if data:
            try:
                bucket_name = data['bucket_name']
                date_created = datetime.datetime.now()
                date_changed = datetime.datetime.now()
            except Exception as e:
                abort(401, message='No bucket data passed')
            
            
            try:
                owner = get_user_name(get_user_id(request.headers.get('Authorization')))
                
                bucketlist = Bucketlist(bucket_name = bucket_name,
                                    date_created = str(date_created),
                                    created_by = owner,
                                    date_modified = str(date_changed)
                                    )
                save_new_bucketlist(bucketlist, request.headers.get('Authorization'))
                
                return jsonify({
                    'message':'New Bucketlist created',
                    'status_code':200
                    })

            except Exception as e:
                abort(401, message='Invalid or Missing access token ')
            
        else:
            abort(401, message='No bucketlist data passed.')
    
class ListBucketlist(Resource):
    
    def get(self, bucket_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        try:
            bucket = get_bucketlist(
                get_user_id(request.headers.get('Authorization')),
                bucket_id
            )

            return jsonify({"bucket": bucket})
        except Exception as e:
            return jsonify(
                {
                    'message':'Bucket doesn\'t exist',
                    'status_code':404
                })
    
    def put(self,bucket_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        data = json.loads(request.get_data())
        if data:
            try:
                new_bucket_name = data['new_bucket_name']
            except Exception as e:
                abort(401, message='Missing new data.')

            try:
                bucket = get_bucketlist(
                    get_user_id(request.headers.get('Authorization')),
                    bucket_id
                )
            except Exception as e:
                return jsonify(
                    {
                        'message':'Bucket doesn\'t exist',
                        'status_code':404
                    })
            
            try:
                edited_bucket_list = edit_bucketlist(
                        get_user_id(request.headers.get('Authorization')),
                        bucket_id,
                        new_bucket_name,
                        datetime.datetime.now()
                    )
                    
                return jsonify({
                    'message':'Bucketlist edited successful',
                    'status_code':200
                    })

            except Exception as e:
                abort(401, message='Invalid or Missing access token ')
        else:
            abort(401, message='No bucketlist data passed.')
        
    def delete(self, bucket_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        try:
            bucket = get_bucketlist(
                get_user_id(request.headers.get('Authorization')),
                bucket_id
            )

        except Exception as e:
            return jsonify(
                {
                    'message':'Bucket doesn\'t exist',
                    'status_code':404
                })

        try:
            bucket_deleted = delete_bucketlist(
                get_user_id(request.headers.get('Authorization')),
                bucket_id)

            return jsonify({
                'message':'Bucket deleted successfull.',
                'status_code':200
                })
        except Exception as e:
            return jsonify(
                {
                    'message':'Bucket doesn\'t exist',
                    'status_code':404
                })  
    
class BucketListItem(Resource):
    
    def get(self, bucket_id):
        return jsonify({"message":"Create a new bucket item by sending"
                        " POST request to /bucketlists/<int:bucket_id>/items."})

    def post(self, bucket_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        data = json.loads(request.get_data())
        if data:
            try:
                new_item_name = data['item_name']
                date_created = datetime.datetime.now()
                date_modified = datetime.datetime.now()
                task_done = data['task_done'] or 'False'
            except Exception as e:
                abort(401, message='No bucketlist item data passed.')
            
            
            if new_item_name:
                try:
                    bucket = get_bucketlist(
                        get_user_id(request.headers.get('Authorization')),
                        bucket_id
                    )
                except Exception as e:
                    return jsonify(
                        {
                            'message':'Bucket doesn\'t exist',
                            'status_code':404
                        })

                bucket_item = Bucket_items(
                                item_name = new_item_name,
                                date_created = str(date_created),
                                date_modified = str(date_modified),
                                task_done = task_done
                                )
                save_new_bucketlist_item(
                    bucket_item,
                    get_user_id(request.headers.get('Authorization')),
                    bucket_id)
                    

                return jsonify({
                        'message':'New Bucketlist item created',
                        'status_code':200
                        })
                
            else:
                abort(401, message='Cannot create item with empty name.')
                
        else:
            abort(401, message='No bucketlist data passed.')

    def put(self, bucket_id):
        return jsonify({"message":"Create a new bucket item by sending"
                        " POST request to /bucketlists/<int:bucket_id>/items."})

    def delete(self, bucket_id):
        return jsonify({"message":" Create a new bucket item by sending"
                        " POST request to /bucketlists/<int:bucket_id>/items."})

class ListBucketlistItem(Resource):
    
    def get(self, bucket_id, item_id):
        return jsonify({"message":"Update an existing bucket item by sending"
                        " PUT request to /bucketlists/<int:bucket_id>/items/<int:item_id>." 
                        " Delete an existing bucket item by sending" 
                        " DELETE request to /bucketlists/<int:bucket_id>/items/<int:item_id>." })

    def post(self, bucket_id, item_id):
        return jsonify({"message":"Update an existing bucket item by sending"
                        " PUT request to /bucketlists/<int:bucket_id>/items/<int:item_id>." 
                        " Delete an existing bucket item by sending" 
                        " DELETE request to /bucketlists/<int:bucket_id>/items/<int:item_id>." })

    def put(self, bucket_id, item_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        data = json.loads(request.get_data())
        if data:
            try:
                new_item_name = data['new_item_name']
                task_done = data['task_done'] or 'False'
            except Exception as e:
                abort(401, message='Missing new data.') 
            
            try:
                bucket = get_bucketlist(
                    get_user_id(request.headers.get('Authorization')),
                    bucket_id
                )
            except Exception as e:
                return jsonify(
                    {
                        'message':'Bucket doesn\'t exist',
                        'status_code':404
                    })
            try:
                if get_specific_bucket_item(bucket_id, item_id):
                    pass
                else:
                    return jsonify(
                        {
                            'message':'Bucket item doesn\'t exist',
                            'status_code':404
                        })
            except Exception as e:
                return jsonify(
                    {
                        'message':'Bucket item doesn\'t exist',
                        'status_code':404
                    })

            try:
                edited_bucket_list = edit_bucket_item(
                    user_id = get_user_id(request.headers.get('Authorization')),
                    bucket_id = bucket_id,
                    item_id = item_id,
                    new_name = new_item_name,
                    task_done = task_done,
                    modified_time= datetime.datetime.now()
                    )
                    
                return jsonify({
                    'message':'Bucketlist item edited successful',
                    'status_code':200
                    })

            except Exception as e:
                abort(401, message='Invalid or Missing access token ')
                
        else:
            abort(401, message='No bucketlist items data passed.')
        
    def delete(self, bucket_id, item_id):

        try:
            get_user_id(request.headers.get('Authorization'))
        except Exception as e:
            abort(401, message='Access forbidden, Login to continue.')

        try:
            bucket = get_bucketlist(
                get_user_id(request.headers.get('Authorization')),
                bucket_id
            )

        except Exception as e:
            return jsonify(
                {
                    'message':'Bucket doesn\'t exist',
                    'status_code':404
                })

        try:
            if get_specific_bucket_item(bucket_id, item_id):
                pass
            else:
                return jsonify(
                    {
                        'message':'Bucket item doesn\'t exist',
                        'status_code':404
                    })

        except Exception as e:
            return jsonify(
                        {
                            'message':'Bucket item doesn\'t exist',
                            'status_code':404
                        })

        deleted_bucket_list_item = delete_bucket_list_item(
            user_id=get_user_id(request.headers.get('Authorization')),
            bucket_id = bucket_id,
            item_id = item_id)

        return jsonify({
            'message':'Bucket deleted successfull.',
            'status_code':200
            })
    

