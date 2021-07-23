import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date

casting_assistant_auth_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGI1NjNmNTk2ZmM3MzAwNjk0M2M3NDYiLCJhdWQiOiJDYXN0aW5nIFNlcnZpY2UiLCJpYXQiOjE2MjcwNzk0NzEsImV4cCI6MTYyNzA4NjY3MSwiYXpwIjoibkJFZ2x4bERTTnRrVzMzcFZ1TnlGWXBYaFBkejZQekciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.BU0cPoISYvcIjO717D_A2cEFuUGm2DZkIAlZoLmYo3P4fPJd-v4p8lJUjh6vEN64HnNu7awfpP-slxKVfOzxD3HKv021U42MizHcpUU__HiMdrY0gbtzYby4EIadaxgu0IXemN84w6uhAsX2CUagVUAiMWoLod4SC-_cB8Xubk4pYXs7AXQ3xmSrYx9s_hb350etRtDDvd1dcsNr3YYOTEybULKGhXszrUNLmSLFfgQbWDKkKSyFyeLaDYNvtxEtKLPaYFQrGC3OLD-SH1Bn0f4KgoN6qmrIXDowhZqF3HEUyWPv2M6hwJu_pjF9Y5igCGTR5EPfr2GS68qW5FDDSg'

casting_director_auth_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGJkNGExZWQwMmY2NTAwNjk1YWFiMGMiLCJhdWQiOiJDYXN0aW5nIFNlcnZpY2UiLCJpYXQiOjE2MjcwNzk2ODMsImV4cCI6MTYyNzA4Njg4MywiYXpwIjoibkJFZ2x4bERTTnRrVzMzcFZ1TnlGWXBYaFBkejZQekciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.aEUC_A6-yh6ngg_onx97B43nArdDLiq5DlH8U7KHwx9j-S83OCoE9dP6JJlLE-gWWW4NUuSCXZruBFrsyNiz_fsO_fvNUQ7uQZi8rK8e0jkiCmCX4lFG853qyb3eDInET5FiehhS1EwcGOrVmKLlZ0Csvtn1b37fzoqGmhuEKcJZNjh_jrVTXe0BL1pHID6Cg4X9DLP9cwOW9BRUM-0o0lVsGCkxAtFojx4ovnY1RAm-arborcjM8NtX131WXVwVHWC1If6oN0IEZNE7I-hQ5xl9C-QYZPZfm_OLjjh8K2mWK5jyyYhMSlPA8jqm8diSLAtU5BwoWfQjykGp1IL1tA'

executive_producer_auth_header = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5HSi1MNTJCMFU3UnZGeVJxUnlXZiJ9.eyJpc3MiOiJodHRwczovL3VkYWNmc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwODI2MzYzNDUzNjk5MDQwNzUwNCIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE2MjcwODM1MzQsImV4cCI6MTYyNzA5MDczNCwiYXpwIjoibkJFZ2x4bERTTnRrVzMzcFZ1TnlGWXBYaFBkejZQekciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.ThTbmKYTxyHAVqMzIYnaULWywaTFIXHgmdkmpHBA9AQoCFdlfJCt2DoHpidjO2BxxkjeaKtA_M4m7DUMg93ecfau1ZppGuS7ThDdBjNc5Gy8dRdBKL99ZNzZ1HMq1-Egs0TnIIGiJMtnId-ihJJQr2c3hBx5SmuA6EoM9gsHOFWGguUWheOhJry1lMz9ifpx3jN6xtdcwU8YPARO3HFOTj1c-f99W729g50aIjNy9hVOyiLRCN8d0o6HNHwLq6dvEWovwYuh3AOO-KdDFFzcgSNcK1ddx0KCm5Iy_Ddk_udPJQFlc86L72wIX6xhhXhx2uqgvW2gH45iq2l2enU1FA'

class CastingTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        
    def tearDown(self):
        pass

    
    #Retrieve Movies Tests

    # Retrieve movies with authorization
    def test_retrieve_movies(self):
        res = self.client().get('/movies?page=1', headers ={'Authorization': 'Bearer' +  casting_assistant_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.asserTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    #Retrieve movies with no authorization
    def test_retreive_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing')
    
    #Retrieve movies error test - no movies
    def test_retrieve_movies_404(self):
        res = self.client().get('/movies?page=5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No movies found')

    #Retreive Actors tests

    # Retreive actors with authorization
    def test_retrieve_actors(self):
        res = self.client().get('actors?page=1', headers ={'Authorization': 'Bearer' +  casting_assistant_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Retrieve actors without authorization
    def test_retrieve_actors_no_auth(self):
        res = self.client().get('actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing')

    #Retrieve actors error test - no actors in database
    def test_retreive_actors_404(self):
        res = self.client().get('actors?page=5000', headers ={'Authorization': 'Bearer' +  casting_assistant_auth_header})
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'no actors found')

    #Insert actors tests

    # Insert actor with authorization
    def test_insert_actor_with_auth(self):
        json_new_actor = {
            'name': 'Idris Elba',
            'age': '48',
            'gender': 'male'
        }
        
        res = self.client().post('/actors', json=json_new_actor, headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 1)
    
    #Insert actor no authorization
    def test_insert_actor_no_auth(self):
        json_new_actor = {
            'name': 'Idris Elba',
            'age': 48,
            'gender': 'male'
        }

        res = self.client().post('/actors', json=json_new_actor)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is missing')

    #insert actor missing form data
    def test_insert_actor_missing_form_data(self):
        json_new_actor = {
            'name': '',
            'age': 48,
            'gender': 'male',
        }

        res = self.client().post('/actors', json=json_new_actor, headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Name field is blank')

    #patch actor with auth
    def test_patch_actor(self):
        json_patch_actor_name = {
            'name': 'Idris Albo'
        }

        res = self.client().patch('/actors/1', json = json_patch_actor_name, headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.asserTrue(len(data['actor'])> 0)
        self.assertEqual(data['updated'], 1)

    #patch actor no auth
    def test_patch_actor_no_auth(self):
        json_patch_actor_name = {
            'name': 'Idris Albo'
        }

        res = self.client().patch('/actors/1', json = json_patch_actor_name)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization Header is missing')
    
    #patch actor no actor in database
    def test_patch_actor_no_data(self):
        json_patch_actor_404 = {
            'age': '55'
        }

        res = self.client().patch('/actors/50000', json = json_patch_actor_404, headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid actor Id - actor not found')


    #delete actor with auth and permissions
    def test_delete_actor_with_auth(self):
        res = self.client().delete('/actors/1', headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')
    
    #delete actor with missing permissions
    def test_delete_actor_no_permission(self):
        res = self.client().delete('/actors/1', headers ={'Authorization': 'Bearer' +  casting_assistant_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permissions missing')

    #delete actor not in database error
    def test_delete_actor_404(self):
        res = self.client().delete('/actors/500000', headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Actor not found in database' )
        

    #insert movie with auth
    def test_insert_movie_with_auth(self):
        json_insert_movie = {
            'title': 'Castaway 2',
            'release_date': date.today()
        }

        res = self.client().post('/movies', json = json_insert_movie, headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['created'], 2)

    #insert movie no auth
    def test_insert_movie_no_auth(self):
        json_insert_movie = {
            'title': 'Castaway 2',
            'release_date': date.today
        }

        res = self.client().post('/movies', json = json_insert_movie)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header missing')

    #insert movie missing permissions
    def test_insert_movie_no_permission(self):
        json_insert_movie = {
            'title': 'Castaway 2',
            'release_date': date.today()
        }

        res = self.client().post('/movies', json = json_insert_movie, headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header missing')

    #insert movie missing form data
    def test_insert_movie_missing_form_data(self):
        json_insert_movie = {
            'title': '',
            'release_date': date.today()
        }
        
        res = self.client().post('/movies', json = json_insert_movie, headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Title field is blank')

    #patch movie with auth

    def test_patch_movie_with_auth(self):
        json_patch_movie = {
            'title': 'Castaway 3'
        }

        res = self.client().patch('/movies/2', json = json_patch_movie, headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], '2')
    
    #patch movie no auth
    def test_patch_movie_no_auth(self):
        json_patch_movie = {
            'title': 'Castaway 3'
        }

        res = self.client().patch('/movies/2', json = json_patch_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header missing')
    
    #patch movie no permissions
    def test_patch_movie_no_permissions(self):
        json_patch_movie = {
            'title': 'Castaway 3'
        }

        res = self.client().patch('/movies/2', json = json_patch_movie, headers ={'Authorization': 'Bearer' +  casting_assistant_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Missing permissions')
    
    #patch movie 404 error 
    def test_patch_movie_404(self):
        json_patch_movie = {
            'title': 'Castaway 4'
        }

        res = self.client().patch('/movies/5000000', json = json_patch_movie, headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Movie not found in database')

    #delete movie with authorization
    def test_delete_movie_with_auth(self):
        res = self.client().delete('/movies/2', headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '2')

    #delete movie no authorization
    def test_delete_movie_no_auth(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)
    
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header missing')

    #delete movie no permissions
    def test_delete_movie_no_permission(self):
        res = self.client().delete('/movies/2', headers ={'Authorization': 'Bearer' + casting_director_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'No permissions found')

    #delete movie 404 
    def test_delete_movie_404(self):
        res = self.client().delete('/movies/500000', headers ={'Authorization': 'Bearer' + executive_producer_auth_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Movie not found in database')

if __name__=="__main__":
    unittest.main()    
