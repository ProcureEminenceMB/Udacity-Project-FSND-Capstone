import os
import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):

	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	# Routes
	@app.route('/actors', methods=['GET'])
	def get_actors():
		try:
			actorList = Actor.query.all()

			if len(actorList) > 0:
				return jsonify({
					'success': True,
					'actors': [actor.short() for actor in actorList],
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
			abort(404)

	@app.route('/movies', methods=['GET'])
	def get_movies():
		try:
			movieList = Movie.query.all()

			if len(movieList) > 0:
				return jsonify({
					'success': True,
					'movies': [movie.short() for movie in movieList],
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
			abort(404)

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