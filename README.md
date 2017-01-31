[![Build Status](https://travis-ci.org/andela-marvin-kangethe/Andela-Bucket_List_Program.svg?branch=master)](https://travis-ci.org/andela-marvin-kangethe/Andela-Bucket_List_Program)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2a978343705e41d1b80777607105cde7)](https://www.codacy.com/app/marvin-kangethe/Andela-Bucket_List_Program?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-marvin-kangethe/Andela-Bucket_List_Program&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/2a978343705e41d1b80777607105cde7)](https://www.codacy.com/app/marvin-kangethe/Andela-Bucket_List_Program?utm_source=github.com&utm_medium=referral&utm_content=andela-marvin-kangethe/Andela-Bucket_List_Program&utm_campaign=Badge_Coverage)
[![Code Health](https://landscape.io/github/andela-marvin-kangethe/Andela-Bucket_List_Program/master/landscape.svg?style=plastic)](https://landscape.io/github/andela-marvin-kangethe/Andela-Bucket_List_Program/master)
# Andela-Bucket_List_Program
This program is a Flask API program used to create bucketlist for storing items of interest.

| Endpoint                 				               		   | Functionality 						 |    
| -------------------------------------------------------------|:-----------------------------------:|
| `POST /auth/login`         				                   |  Logs a user in                     |
| `POST /auth/register`      				                   |  Register a user                    |
| `POST /bucketlists/`       				                   |  Create a new bucket list	         |
| `GET /bucketlists/`						                   |  List all the created bucket lists	 | 
| `GET /bucketlists/<bucket_id>`		                   |  Get single bucket list             |                     
| `PUT /bucketlists/<bucket_id> `                         |  Update this bucket list            |                       
| `DELETE /bucketlists/<bucket_id>`				       |  Delete this single bucket list     |                              
| `POST /bucketlists/<bucket_id>/items`                   |  Create a new item in bucket list   |                                
| `PUT /bucketlists/<bucket_id>/items/<item_id>`          |  Update a bucket list item          |                         
| `DELETE /bucketlists/<bucket_id>/items/<item_id>`       |  Delete an item in a bucket list    |

##Options

| Endpoint                 				               		   | Functionality 						 	  |    
| -------------------------------------------------------------|:----------------------------------------:|
| `SEARCH /bucketlists?q=abc`         				           | Enter a search parameter                 |
| `PAGENATION /bucketlists?start=0&limit=2`      				 | Start index of current page and number of items per page(default is 20)  |


| Method                 				               		   | Description 						 	  |    
| -------------------------------------------------------------|:----------------------------------------:|
| GET         				           						   | Retrieves a resource(s)                 |
| POST      				                                   | Creates a new resource                  |
| PUT         				                                   | Updates an existing resource            |
| DELETE      				                                   | Deletes an existing resource            |


##Installation
1. Create a working directory.

    	mkdir <name_of_folder>
    
2. Clone this repository.

    * via HTTPS

    	- https://github.com/andela-marvin-kangethe/Andela-Bucket_List_Program.git

    * via SSH

    	- git@github.com:andela-marvin-kangethe/Andela-Bucket_List_Program.git

3. Navigate to project directory.

		cd Andela-Bucket_List_Program/ 
    
4. Create a virtual environment.
    
    	virtualenv <name_of_venv>
      **Advisable to use python 2.7**
    
5. Change working project version
      
        git checkout develop
        
6. Set up the environment requirements.
    
    	pip install -r requirements.txt


7. Initialize, migrate and update the database.
	
		python run.py db init
		python run.py db migrate
		python run.py db upgrade

8. Test the application by running the following command.
	
		nosetests -v

9. Test the application coverage by running the following command.
	
		nosetests --with-coverage --cover-inclusive --cover-package=app/ 
    
10. Run the server.
    
    	python run.py runserver

##Sample Api Use Case
Access the endpoints using your preferred client e.g Postman

- POST http://127.0.0.1:5000/api/v1/auth/register will prompt you to register a new user, providing username, email and password

	body
	
		{
			"username":"John",
			"email":"john@andela.com",
			"password":"12345cv"
		}

 	response

		{
		  	'message':'Registration successfull',
        		'Authorization':GENERATED ACCESS TOKEN
		}

- POST http://127.0.0.1:5000/api/v1/auth/login will login user and generate a token.
	
		{
		 	'message':'login successful',
			'status_code':200,
			'Authorization':GENERATED ACCESS TOKEN
		}

- POST http://127.0.0.1:5000/api/v1/bucketlists/ create a new bucket list
	
	header

		Authorization : GENERATED ACCESS TOKEN 
	
	body

		{   
			"bucket_name":"Python"
		}

	response

		{
		  	"message": "New Bucketlist created",
       			"status_code": 200
		}

- GET http://127.0.0.1:5000/api/v1/bucketlists/ displays all of the users bucket lists.

	header

		Authorization : GENERATED ACCESS TOKEN 

	response

	      {
		  "bucketlists":[
		      {
			  "next": "http://127.0.0.1:5000/api/v1/bucketlists?start=0&limit=20"
		      },
		      {
			  "back": "http://127.0.0.1:5000/api/v1/bucketlists?start=0&limit=20"
		      },
		      {
			  "bucket_id": 7,
			  "bucket_items": [],
			  "bucket_name": "Python",
			  "bucket_owner_id": 2
		      }
		  ]
	       }
- POST http://127.0.0.1:5000/api/v1/bucketlists/{bucket_id}/items create a new item in a bucket list
	
	header

		Authorization : GENERATED ACCESS TOKEN 

	body

		{   
			"item_name":"Django framework",
			"task_done":"False"
		}

	response

		{   
			'message':'New Bucketlist item created',
      			'status_code':200
	   	}
