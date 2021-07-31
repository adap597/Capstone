# Intro

The Casting Agency API models a company responsible for creating movies and managing and assigning actors to those movies. The API allows users to query the database for movies and actors. There are three user roles and associated permissions:
- Casting assistant: Can view actors and movies.
- Casting director: Can view, add, modify, or delete actors; can view and modify movies.
- Executive producer: Can view, add, modify, or delete actors and movies. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup

With Postgres running, restore the database using the casting.psql file provided. In terminal run:

```bash
createdb capstone
psql capstone < capstone.psql
```

#### Running Tests
To run the tests, run
```bash
dropdb casting_test
createdb casting_test
psql casting_test < casting.psql
python test_app.py
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system used to handle users with different roles.

- [PostgreSQL](https://www.postgresql.org/) is the relational dartabase used for this project. 

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment.

#### Auth0 Setup

You need to setup an Auth0 account and create an Application and an API for your application.

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" 
export ALGORITHMS="RS256"
export API_AUDIENCE="Casting" 
```
Note: When you are testing the application on your local machine, the Login, Logout, and Allowed callback URLs in your application should be something like

```
https://127.0.0.1:5000/login
https://127.0.0.1:5000/login-results
https://127.0.0.1:5000/logout
```

Once you are ready to deploy to Heroku, you must change the Login, Logout, and Allowed callback URL to reference the Heroku app.
```
https://{{NAME_OF_YOUR_APP}}.herokuapp.com/login
https://{{NAME_OF_YOUR_APP}}.herokuapp.com/login-results
https://{{NAME_OF_YOUR_APP}}.herokuapp.com/logout
```
##### Roles

Create three roles for users under `Users & Roles` section in Auth0

* Casting Assistant
	* Can view actors and movies
* Casting Director
	* All permissions a Casting Assistant has and…
	* Add or delete an actor from the database
	* Modify actors or movies
* Executive Producer
	* All permissions a Casting Director has and…
	* Add or delete a movie from the database

##### Permissions

Following permissions should be created under created API settings.

* `get:actors`
* `get:movies`
* `delete:actors`
* `post:actors`
* `patch:actors`
* `patch:movies`
* `post:movies`
* `delete:movies`


Use the following link to sign in each user after you have assigned roles and permissions. This will generate tokens. 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```
#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   source env/bin/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
        database_filename = "casting"
        project_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = "postgresql:///{}".format(database_filename)
    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. 


4. Setup the environment variables for Auth0 under `setup.sh` running:
	```bash
	source ./setup.sh 
	```
5.  To run the server locally, execute:

    ```bash
    export FLASK_APP=app
    export FLASK_DEBUG=True
    export FLASK_ENVIRONMENT=debug
    flask run --reload
    ```

## API Documentation

### Base URL

https://git.heroku.com/casting-app-capstone.git

### Models
There are two models:
* Movie
	* title
	* release_date
* Actor
	* name
	* age
	* gender

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Unprocessable 
- 500: Internal Server Error

### Endpoints


#### GET /movies 
* Get all movies

* Require `get:movies` permission

* **Expected Result:**
```json
    {
    "movies": [
        {
            "id": 1,
            "release_date": "May 2, 2011",
            "title": "Thor"
        },
        {
            "id": 3,
            "release_date": "May 23, 1980,
            "title": "The Shining"
        }

    ],
    "success": true
    }
```
	
#### GET /actors 
* Get all actors

* Requires `get:actors` permission

* **Expected Result:**
    ```json
	{
		"actors": [
			{
			"age": 48,
			"gender": "M",
			"id": 1,
			"movie_id": 1,
			"name": "Idris Elba"
			},
			{
			"age": 84,
			"gender": "M",
			"id": 2,
			"movie_id": 2,
			"name": "Jack Nicholson"
			}
		],
		"success": true
	}
	```
	
#### POST /movies
* Creates a new movie.
* Requires `post:movies` permission
* Requires the title and release date.

```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```

#### POST /actors
* Creates a new actor.
* Requires `post:actors` permission
* Requires the name, age and gender of the actor.

```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```

#### DELETE /movies/<int:movie_id>
* Deletes the movie with given id 
* Require `delete:movies` permission
* Request argument: Movie id, included as a parameter following a forward slash (/).
* Returns: ID for the deleted movie and status code of the request.

```
{
	'id': 5,
	'success': true
}
```
    
#### DELETE /actors/<int:actor_id>
* Deletes the actor with given id 
* Require `delete:actors` permission
* Request argument: Actor id, included as a parameter following a forward slash (/).
* Returns: ID for the deleted actor and status code of the request.

```
{
	'id': 5,
	'success': true
}
```

#### PATCH /movies/<movie_id>
* Updates the movie where <movie_id> is the existing movie id
* Require `patch:movies` permission
* Responds with a 404 error if <movie_id> is not found
* Update the corresponding fields for Movie with id <movie_id>

```
{
	"release": "November 3, 2017"
}
```
  
* **Example Response:**
```
{
    "movie": {
        "id": 5,
        "release": "November 3, 2017",
        "title": "Thor: Ragnarok"
    },
    "success": true
}
```
	
#### PATCH /actors/<actor_id>
* Updates the actor where <actor_id> is the existing actor id
* Require `patch:actors`
* Responds with a 404 error if <actor_id> is not found
* Update the given fields for Actor with id <actor_id>
```
{
	"age": "36"
}
```
  
* **Example Response:**
```
{
    "actor": {
        "age": "36",
        "gender": "male",
        "id": 6,
        "name": "Henry Cavill"
    },
    "success": true
}
```

