import os
import json
import datetime

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):

	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	# GET Routes
	@app.route('/actors', methods=['GET'])
	@requires_auth('get:actors')
	def get_actors():
		try:
			# Get a list of all actors in DB
			actorList = Actor.query.all()

			# Return the list of actors if at least one exists
			if len(actorList) > 0:
				return jsonify({
					'success': True,
					'actors': [actor.format() for actor in actorList],
					'actor_count': len(actorList)
				}), 200

			else:
				return jsonify({
					'success': False,
					'actors': [],
					'actor_count': 0,
					'message': 'No actors found.'
				}), 200

		except Exception:
			# Return Unprocessable Entity error if the Try block fails
			abort(422)

	@app.route('/movies', methods=['GET'])
	@requires_auth('get:movies')
	def get_movies():
		try:
			# Get a list of all movies in DB
			movieList = Movie.query.all()

			# Return the list of movies if at least one exists
			if len(movieList) > 0:
				return jsonify({
					'success': True,
					'movies': [movie.format() for movie in movieList],
					'movie_count': len(movieList)
				}), 200

			else:
				return jsonify({
					'success': False,
					'movies': [],
					'movie_count': 0,
					'message': 'No movies found.'
				}), 200

		except Exception:
			# Return Unprocessable Entity error if the Try block fails
			abort(422)
	# END GET Routes

	# POST Routes
	@app.route('/actors', methods=['POST'])
	@requires_auth('post:actors')
	def add_actor():
		body = request.get_json()

		try:
			name = body.get('name', None)
			age = int(body.get('age', 0))
			gender = body.get('gender', None)

			if name and age > 0 and gender:
				actor = Actor(
					name = name,
					age = age,
					gender = gender)

				try:
					actor.insert()

				except Exception:
					abort(422)

				return jsonify({
					'success': True,
					'actor_id': actor.id,
					'actor_name': actor.name,
					'actor_age': actor.age,
					'actor_gender': actor.gender
				})

			else:
				abort(400)

		except Exception:
			# Return Unprocessable Entity error if the Try block fails
			abort(422)

	@app.route('/movies', methods=['POST'])
	@requires_auth('post:movies')
	def add_movie():
		body = request.get_json()

		try:
			title = body.get('title', None)
			release_date = body.get('release_date', None)

			if title and release_date:
				date_details = release_date.split('-')
				year = int(date_details[0])
				month = int(date_details[1])
				day = int(date_details[2])

				movie = Movie(
					title = title,
					release_date = datetime.datetime(year, month, day))

				try:
					movie.insert()

				except Exception:
					abort(422)

				return jsonify({
					'success': True,
					'movie_id': movie.id,
					'movie_title': movie.title,
					'movie_release_date': movie.release_date
				})

			else:
				abort(400)

		except Exception:
			# Return Unprocessable Entity error if the Try block fails
			abort(422)
	# END POST Routes

	# PATCH Routes
	@app.route('/actors/<int:id>', methods=['PATCH'])
	@requires_auth('patch:actors')
	def patch_actors(id):
		# Get actor details for the matching ID
		actor = Actor.query.get(id)

		try:
			# Loop through updated keys and update the values
			for attribute, value in request.json.items():
				setattr(actor, attribute, value)

			# Push updated values to the DB
			actor.update()

			# Return all actor details after update is completed
			return jsonify({
				'success': True,
				'actor_id': actor.id,
				'actor_name': actor.name,
				'actor_age': actor.age,
				'actor_gender': actor.gender
			}), 200

		except Exception:
			# Return Not Found error if the Try block fails
			abort(404)

	@app.route('/movies/<int:id>', methods=['PATCH'])
	@requires_auth('patch:movies')
	def patch_movies(id):
		# Get movie details for the matching ID
		movie = Movie.query.get(id)

		try:
			# Loop through updated keys and update the values
			for attribute, value in request.json.items():
				# If the actors attribute is found, reference the actors DB table
				if attribute == 'cast':
					setattr(movie, attribute, ",".join(str(actor_id) for actor_id in value))

				else:
					setattr(movie, attribute, value)

			# Push updated values to the DB
			movie.update()

			return jsonify({
				'success': True,
				'movie_id': movie.id,
				'movie_title': movie.title,
				'movie_release_date': movie.release_date,
				'movie_cast': movie.cast
			}), 200

		except Exception:
			# Return Not Found error if the Try block fails
			abort(404)
	# END PATCH Routes

	# DELETE Routes
	@app.route('/actors/<int:id>', methods=['DELETE'])
	@requires_auth('delete:actors')
	def delete_actors(id):
		# Get actor details for the matching ID
		actor = Actor.query.get(id)

		try:
			# Delete entry from the DB
			actor.delete()

			return jsonify({
				'success': True,
				'actor_id': id
			}), 200

		except Exception:
			# Return Not Found error if the Try block fails
			abort(404)

	@app.route('/movies/<int:id>', methods=['DELETE'])
	@requires_auth('delete:movies')
	def delete_movies(id):
		# Get movie details for the matching ID
		movie = Movie.query.get(id)

		try:
			# Delete entry from the DB
			movie.delete()

			return jsonify({
				'success': True,
				'movie_id': id
			}), 200

		except Exception:
			# Return Not Found error if the Try block fails
			abort(404)
	# END DELETE Routes

	# Error Handling
	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			"success": False,
			"error": 400,
			"message": "Bad Request"
		}), 400

	@app.errorhandler(401)
	def unauthorized(error):
		return jsonify({
			"success": False,
			"error": 401,
			"message": "Unauthorized"
		}), 401

	@app.errorhandler(403)
	def forbidden(error):
		return jsonify({
			"success": False,
			"error": 403,
			"message": "Forbidden"
		}), 403

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False,
			"error": 404,
			"message": "Not Found"
		}), 404

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			"success": False,
			"error": 422,
			"message": "Unprocessable Entity"
		}), 422

	@app.errorhandler(AuthError)
	def handle_auth_error(error):
		return jsonify({
			"success": False,
			"error": error.status_code,
			'message': error.error
		}), 401

	return app

# Create and run the app
app = create_app()

if __name__ == '__main__':
	app.run()