
import os
import unittest
# from simplejson import dumps
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all
from sqlalchemy import desc
from datetime import date


casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGI1NjNmNTk2ZmM3MzAwNjk0M2M3NDYiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNjI3MzQyNTQyLCJleHAiOjE2MjczNDk3NDIsImF6cCI6Im5CRWdseGxEU050a1czM3BWdU55RllwWGhQZHo2UHpHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Xegs6kkurtOHbyBfbdb4V6EsrOxzlQnXpHXXK5Ye-rsBcuTDfoJbsNndn5mNcyWkBz-tRGf6pexL91V1vJt5k45b0GEj8buuESZS84eRsD64iz0E6e_CklZBDpiY-RhHWaKOTl5uoVlDkGt9fD42Xup1iYrmohflXrq4kJbxafWTQHLbitMe-cpGgJ5evCLvIz3DgGt7J3oI3XetNxjCm_ACazLDKAhvFa5v4-LywSN2tapuz6RT5OlgrJYHAOyL9ujoOjC3D4ecyhi4eInEiu8LRIMJ9s9lTIyBmH4a7c9bHzAG2nak6op8VDtojRItH9oZqnPYbWgTYnOD9h8X-g'
casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGJkNGExZWQwMmY2NTAwNjk1YWFiMGMiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNjI3MzQyNjY4LCJleHAiOjE2MjczNDk4NjgsImF6cCI6Im5CRWdseGxEU050a1czM3BWdU55RllwWGhQZHo2UHpHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.MAvbYKZZXde3vqBZxsfanzPMd_6gGKLcwwsvoxSCMXQBL2yhkLz8s-8Fa72cWvFG--pohUcQP2QS-ANF5F5pYSjNYDunTUq5NkOOOtFOA2pn66NlNu8gqcEQUhe0q7wM3p8ALcI8YpNd8a2irNTmKfdd0OXwefh5RaAE5KYoMK7Sq4J6Ebo1raaru1Zz_XCQKKNx-I2oCX9Ku6bZKtqKLioeVjZfisOqBQ2RsMQrlEmQHssSdZ48bKvkMmtf1TqTdHysI7ErQh61arA_dIEgAdR9dYRjNll7mEhlMtoGH4sc8RBfavKDxEjta4mij0Jcw-QWQsDUXkU4w_zhxjdAFw'
executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODI2MzYzNDUzNjk5MDQwNzUwNCIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE2Mjc3NzMxODAsImV4cCI6MTYyNzc4MDM4MCwiYXpwIjoibkJFZ2x4bERTTnRrVzMzcFZ1TnlGWXBYaFBkejZQekciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.xTxJLRYAPowec8VDHYkFGT37u13tck4rTrCvw2YX36gwxuU-Qr98rND0grgu53pmHnu7KAmsTgJI5FUUayaNM0F5hhyd03Xj2nNaLRjo5p49F0QSY2vLozubvUhlqw5SdrJ_NEIQm4BxMLfx5ZYD4QC_aU9DBmTHVYlsS0yIH9fP8RykRIOyW0SVxs4hW7QmaYlULmQa9HiSbPijk6CTJW-M11RTtJ-CMkN44S-DkZNn5rTXfedCRzx30nsVa3dfqJ5ymeEh3LEfn_fI67-jJ2ny5496UUTl0lmgWGr7gOuGpeE4Cu4x8vEhtZKImM29kiClIWw0faXKq4zQjPs5SA'


class CastingTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_test'
        self.database_path = 'postgresql://adap194567:postgres@localhost:5432/casting_test'
        self.casting_assistant = casting_assistant_token
        self.casting_director = casting_director_token
        self.exec_producer = executive_producer_token
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Retrieve Movies Tests
    # Retrieve movies with authorization

    def test_retrieve_movies(self):
        res = self.client().get('/movies?page=1',
                                headers={'Authorization': 'Bearer {}'.format(self.casting_assistant)})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    # Retrieve movies with no authorization

    def test_retreive_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # Retrieve movies error test - no movies

    def test_retrieve_movies_404(self):
        res = self.client().get('/movies?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Retreive Actors tests

    # Retreive actors with authorization

    def test_retrieve_actors(self):
        res = self.client().get('actors?page=1',
                                headers={'Authorization': 'Bearer {}'.format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Retrieve actors without authorization

    def test_retrieve_actors_no_auth(self):
        res = self.client().get('actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # Retrieve actors error test - no actors in database

    def test_retreive_actors_404(self):
        res = self.client().get('actors?page=5000',
                                headers={'Authorization': 'Bearer {}'.format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Insert actors tests

    # Insert actor with authorization

    def test_insert_actor_with_auth(self):
        json_new_actor = {'name': 'Idris Elba', 'age': '48',
                          'gender': 'male'}

        res = self.client().post('/actors', json=json_new_actor,
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqua(data['success'], True)
        self.assertEqual(data['created'], 1)

    # Insert actor no authorization

    def test_insert_actor_no_auth(self):
        json_new_actor = {'name': 'Idris Elba', 'age': 48,
                          'gender': 'male'}

        res = self.client().post('/actors', json=json_new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # insert actor missing form data

    def test_insert_actor_missing_form_data(self):
        json_new_actor = {'name': '', 'age': 48, 'gender': 'male'}

        res = self.client().post('/actors', json=json_new_actor,
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # patch actor with auth

    def test_patch_actor(self):
        json_patch_actor_name = {'name': 'Idris Albo'}

        res = self.client().patch('/actors/1',
                                  json=json_patch_actor_name,
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.asserTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    # patch actor no auth

    def test_patch_actor_no_auth(self):
        json_patch_actor_name = {'name': 'Idris Albo'}

        res = self.client().patch('/actors/1',
                                  json=json_patch_actor_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # patch actor no actor in database

    def test_patch_actor_no_data(self):
        json_patch_actor_404 = {'age': '55'}

        res = self.client().patch('/actors/50000',
                                  json=json_patch_actor_404,
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # delete actor with auth and permissions

    def test_delete_actor_with_auth(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '1')

    # delete actor with missing permissions

    def test_delete_actor_no_permission(self):
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'forbidden')

    # delete actor not in database error

    def test_delete_actor_404(self):
        res = self.client().delete('/actors/500000',
                                   headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # insert movie with auth

    def test_insert_movie_with_auth(self):
        json_insert_movie = {'title': 'Castaway 2',
                             'release_date': date.today()}

        res = self.client().post('/movies', json=json_insert_movie,
                                 headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 2)

    # insert movie no auth

    def test_insert_movie_no_auth(self):
        json_insert_movie = ({'title': 'Castaway 2',
                              'release_date': '2021-08-25'})

        res = self.client().post('/movies', json=json_insert_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success']), False
        self.assertEqual(data['message'], 'unauthorized'
                         )

    # insert movie missing permissions

    def test_insert_movie_no_permission(self):
        json_insert_movie = {'title': 'Castaway 2',
                             'release_date': '2021-08-25'}

        res = self.client().post('/movies', json=json_insert_movie,
                                 headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'forbidden'
                         )

    # insert movie missing form data

    def test_insert_movie_missing_form_data(self):
        json_insert_movie = {'title': '', 'release_date': date.today()}

        res = self.client().post('/movies', json=json_insert_movie,
                                 headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # patch movie with auth

    def test_patch_movie_with_auth(self):
        json_patch_movie = {'title': 'Castaway 3'}

        res = self.client().patch('/movies/2', json=json_patch_movie,
                                  headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], '2')

    # patch movie no auth

    def test_patch_movie_no_auth(self):
        json_patch_movie = {'title': 'Castaway 3'}

        res = self.client().patch('/movies/2', json=json_patch_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized'
                         )

    # patch movie no permissions

    def test_patch_movie_no_permissions(self):
        json_patch_movie = {'title': 'Castaway 3'}

        res = self.client().patch('/movies/2', json=json_patch_movie,
                                  headers={'Authorization': 'Bearer {}'.format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'forbidden')

    # patch movie 404 error

    def test_patch_movie_404(self):
        json_patch_movie = {'title': 'Castaway 4'}

        res = self.client().patch('/movies/5000000',
                                  json=json_patch_movie,
                                  headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # delete movie with authorization

    def test_delete_movie_with_auth(self):
        res = self.client().delete('/movies/2',
                                   headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')

    # delete movie no authorization

    def test_delete_movie_no_auth(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    # delete movie no permissions

    def test_delete_movie_no_permission(self):
        res = self.client().delete('/movies/2',
                                   headers={'Authorization': 'Bearer {}'.format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'forbidden')

    # delete movie 404

    def test_delete_movie_404(self):
        res = self.client().delete('/movies/500000',
                                   headers={'Authorization': 'Bearer {}'.format(self.exec_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == '__main__':
    unittest.main()
