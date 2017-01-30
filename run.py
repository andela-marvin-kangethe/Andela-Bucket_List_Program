from flask import jsonify
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from flask_restful import Api, Resource

from app import app, db
from app.auth.controller import Register, Login
from app.Bucketlist.bucket import BucketList, ListBucketlist, BucketListItem, ListBucketlistItem

manager = Manager(app)
migrate = Migrate(app, db)

api = Api(app, prefix="/api/v1")

@app.errorhandler(500)
def internal_server_error(e):
	return jsonify({
		'message':'Internal Server Error',
		'status_code':500
		})
@app.errorhandler(404)
def resource_not_found(e):
	return jsonify({
		'message':'Resource Not Found',
		'status_code':404,
		'self help':'Check the url used.'
		})

#Login a registered user	POST
api.add_resource(Login, "/auth/login", endpoint="login")	

#Register an non existing user	POST
api.add_resource(Register, "/auth/register", endpoint="register")

#Get all buckests 	GET
api.add_resource(BucketList, "/bucketlists/", endpoint="viewallbucketlist")

#Get the content of specific id 			GET
#Edit the content of a specific bucket 		PUT
#Delete an existing bucketlist 				DELETE
api.add_resource(ListBucketlist, "/bucketlists/<bucket_id>", endpoint="modifyspecificbucketlist")

#Create a new bucket item for a specific bucket 	POST
api.add_resource(BucketListItem, "/bucketlists/<bucket_id>/items", endpoint="createnewbucketitem")


#Edit the content of a specific bucket item 		PUT
#Delete an existing bucketlist item 				DELETE
api.add_resource(ListBucketlistItem, "/bucketlists/<bucket_id>/items/<item_id>", endpoint="modifyspecificbucketlistitem")


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()

