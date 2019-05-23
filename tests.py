from unittest import TestCase
from server import app 
import googlemaps
import os

class RouteTests(TestCase):

    def setUp(self):
        """Set up elements before every test."""
        self.Client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        """non-database test for home route"""
        results = self.Client.get("/")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Map</h1>', results.data)


    def test_add_art(self):
        """non-database test for add_art route"""
        results = self.Client.get("/add_art")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Add Art Site</h1>', results.data)


    def test_register(self):
        pass


    def test_login(self):
        pass


    def test_post_add_art(self):
        results = self.Client.post('/add_art',
                                   data={
                                   "title": "test title",
                                   "artist": "test artist", 
                                   "artist_desc": "test artist description", 
                                   "street_address": "683 Sutter Street", 
                                   "source": "test",
                                   "medium": "paint", 
                                   "art_desc": "test art description", 
                                   "hint":"test hint"})

        self.assertEqual(results.status_code, 200)

# test cases 
# - user already registered, goes to login route w/ flash message saying already registered 
# - user registers for the first time, goes to login route w/ flash message saying thanks for registering 

# test cases 
# - user in userdb, login and go to homepage 
# - user not in db because go back to login 

# class DatabaseTests(TestCase): 

#     def setUp(self):
#         """Set up elements before every test."""
#         self.Client = app.test_client()
#         app.config['TESTING'] = True


#         connect_to_db(app, "postgresql:///testdb")

#         db.create_all()

#         example_data()



