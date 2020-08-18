import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, database_path

# Test auth headers

assistant_auth_header = {
    'Authorization': 'Bearer ' + os.getenv('ASSISTANT_AUTH_TOKEN')
}

director_auth_header = {
    'Authorization': 'Bearer ' + os.getenv('DIRECTOR_AUTH_TOKEN')
}

producer_auth_header = {
    'Authorization': 'Bearer ' + os.getenv('PRODUCER_AUTH_TOKEN')
}


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # Bind app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

        # Initial db entries
        new_actor = {'name': 'Robin Williams', 'age': '63',
                     'gender': 'Male'}
        self.client().post('/actors/1',
                           json=new_actor,
                           headers=producer_auth_header)
        new_movie = {'title': 'Bicentennial man',
                     'release_date': '1999-12-13'}
        self.client().post('/movies/1',
                           json=new_movie,
                           headers=producer_auth_header)

    def tearDown(self):
        pass

    # Public test cases
    def test_public_get_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_public_get_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Assistant test cases
    def test_assistant_get_actors(self):
        res = self.client().get('/actors',
                                headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_assistant_get_actors(self):
        res = self.client().get('/actors',
                                headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_assistant_create_actor_401(self):
        new_actor = {'name': 'Robin Williams', 'age': '63',
                     'gender': 'Male'}
        res = self.client().post('/actors',
                                 json=new_actor,
                                 headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_create_movie_401(self):
        new_movie = {'title': 'Bicentennial man',
                     'release_date': '1999-12-13'}
        res = self.client().post('/movies',
                                 json=new_movie,
                                 headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_update_actor_401(self):
        update_actor = {'age': '93'}
        res = self.client().patch('/actors/1',
                                  json=update_actor,
                                  headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_update_movie_401(self):
        update_movie = {'cast': [1, 2]}
        res = self.client().patch('/movies/1',
                                  json=update_movie,
                                  headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_delete_actor_401(self):
        res = self.client().delete('/actors/1',
                                   headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_assistant_delete_movie_401(self):
        res = self.client().delete('/movies/1',
                                   headers=assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Director test cases
    def test_director_get_actors(self):
        res = self.client().get('/actors',
                                headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_director_get_actors(self):
        res = self.client().get('/actors',
                                headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_director_create_actor(self):
        new_actor = {'name': 'Robin Williams', 'age': '63',
                     'gender': 'Male'}
        res = self.client().post('/actors',
                                 json=new_actor,
                                 headers=director_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_create_movie_401(self):
        new_movie = {'title': 'Bicentennial man',
                     'release_date': '1999-12-13'}
        res = self.client().post('/movies',
                                 json=new_movie,
                                 headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_director_update_actor(self):
        update_actor = {'age': '93'}
        res = self.client().patch('/actors/1',
                                  json=update_actor,
                                  headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_update_movie(self):
        update_movie = {'cast': [1, 2]}
        res = self.client().patch('/movies/1',
                                  json=update_movie,
                                  headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_delete_actor(self):
        res = self.client().delete('/actors/1',
                                   headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_director_delete_movie_401(self):
        res = self.client().delete('/movies/1',
                                   headers=director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    # Producer test cases
    def test_producer_get_actors(self):  # Failing test case in public section
        res = self.client().get('/actors',
                                headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_get_movies(self):  # Failing test case in public section
        res = self.client().get('/movies',
                                headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_create_actor(self):  # Failing test case in Ass. section
        new_actor = {'name': 'Robin Williams', 'age': '63',
                     'gender': 'Male'}
        res = self.client().post('/actors',
                                 json=new_actor,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_create_movie(self):  # Failing test case in Ass. section
        new_movie = {'title': 'Bicentennial man',
                     'release_date': '1999-12-13'}
        res = self.client().post('/movies',
                                 json=new_movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_update_actor(self):  # Failing test in Director section
        update_actor = {'age': '93'}
        res = self.client().patch('/actors/1',
                                  json=update_actor,
                                  headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_update_movie(self):  # Failing test in Director section
        update_movie = {'cast': [1, 2]}
        res = self.client().patch('/movies/1',
                                  json=update_movie,
                                  headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_delete_actor(self):  # Failing test in Director section
        res = self.client().delete('/actors/1',
                                   headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_producer_delete_movie(self):  # Failing test in Director section
        res = self.client().delete('/movies/1',
                                   headers=producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
