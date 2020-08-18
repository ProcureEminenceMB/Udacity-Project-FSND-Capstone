# Udacity FSND Capstone Project - Casting Agency API

## Motivation
This API was created for the final FSND project.

## Live Server URL
[https://udacity-casting-agency-app.herokuapp.com/](https://udacity-casting-agency-app.herokuapp.com/)

## Local Server Setup Instructions
If you decide to run this API on your own local server, use the following instructions.
1. Install Python 3.7
2. Install GIT
3. Clone this repository
4. Open a CMD window and navigate to the root of the repo directory
5. Create a virtual environment with Python
```py -m venv env```

	- ‘py’ invokes the Python interpreter.
	- ‘-m’ argument tells Python to run a library module as a script.
	- ‘venv’ module creates a lightweight virtual environment with its own Python binary (equivalent to the currently installed Python version) and has its own set of installed Python packages in the current directory.
	- ‘env’ specifies the desired name of the virtual environment.

6. Activate the Flask venv by using the following CMD command.
	```env\Scripts\activate```
7. Install the Python package requirements.
	```pip install -r requirements.txt```
8. Set environment variable to point to the ```app.py``` file via CMD.
	```set FLASK_APP=app.py```
9. Run the server.
```flask run``` 

## Live Server Setup
To replicate the current live server you will need to create a Heroku account, create an app, and then push the local code to your Heroku app server.

## Auth0 Requirements

The following environment variables are included in the ```setup.sh``` for easy testing of the API: AUTH0_DOMAIN, API_AUDIENCE, and ALGORITHMS. You will need to update the containing values if you choose to start your own Auth0 account. The JWTs are located inside the Postman test collection (```udacity-fsnd-capstone.postman_collection.json```).

## API Reference
### GET Endpoints
 - `/actors`
	 - Returns the entire list of actors.
 - `/movies`
	 - Returns the entire list of movies.

### POST Endpoints
- `/actors`
	- Adds a new actor to the database.
- `/movies`
	- Adds a new movie to the database.

### PATCH Endpoints
- `/actors/<int:id>`
	- Updates details regarding a specific actor.
- `/movies/<int:id>`
	- Updates details regarding a specific movie.

### DELETE Endpoints
- `/actors/<int:id>`
	- Removes a specific actor from the database.
- `/movies/<int:id>`
	- Removes a specific movie from the database.

### Roles & Permissions
- Assistant Role
	- `get:actors`
	- `get:movies`
- Director Role
	- `get:actors`
	- `get:movies`
	- `post:actors`
	- `patch:actors`
	- `patch:movies`
	- `delete:actors`
- Producer Role
	- `get:actors`
	- `get:movies`
	- `post:actors`
	- `post:movies`
	- `patch:actors`
	- `patch:movies`
	- `delete:actors`
	- `delete:movies`

## API Endpoint Testing
All testing for this API was accomplished via [Postman](https://www.postman.com/). These tests have been included in this repository in the form of a Postman collection file (`udacity-fsnd-capstone.postman_collection.json`). You can import this collection and run the tests once you have finished setting up your server.
