import unittest
from model import User, Artwork, Add, Log, connect_to_db, db, example_data
from server import app 
import server
from sqlalchemy import func 
from geoalchemy2 import Geometry

# TEST PLAN 
# Backend tests: unittest 
# Testflaskroutesnologin: 

# test_get_homepage_200
# test_get_register_200
# test_post_register_200 
# rest_post_register_invalid_400
# test_get_login_200
# test_post_login_200
# test_post_login_invalid_400

# Testflaskrouteslogin:

# test_post_login_200
# test_logout

# test_get_add_art_200
# test_post_add_art_200
# test_post_add_art_invalid_400

# test_get_profile_200


# TEST EDGE CASES 
# User 
# - user already registered, goes to register, 400 
# - user not register tries to login, 400 
# - user email address/username already registered, 400 
# - user login not in database, 400 
# Artwork 
# - artwork already add (how will i validate for this)
# - artwork does not have required fields 
        # location, hint, or image 



class TestFlaskRoutesNoLogIn(unittest.TestCase):

    def setUp(self):
        """Set up elements before every test."""
        self.Client = app.test_client()
        app.config['TESTING'] = True

        # connect to test database 
        connect_to_db(app, "postgresql:///testdb")

        # create tables and add sample data 
        db.create_all()

    def tearDown(self):
        """Do at the end of every test."""

        db.session.close()
        db.drop_all()


    def test_get_homepage_200(self):
        """GET home route."""
        results = self.Client.get("/")
        self.assertEqual(results.status_code, 200)


    def test_get_register_200(self):
        """GET register route."""
        results = self.Client.get("/register")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'username', results.data)

    def test_post_register_200(self):
        """POST registration form."""
        results = self.Client.post("/register",
                                   data = {"email": "test@test123.com",
                                           "username": "test user",
                                           "password": "test"},
                                    follow_redirects = True)
        self.assertEqual(results.status_code, 200)

    def test_post_register_invalid_400(self):
        """POST an invalid registration form.
        
        user already exists in users table. 
        """
        results = self.Client.post("/register",
                                   data = {"email": "test@test123.com",
                                           "username": "test user",
                                           "password": "test"},
                                    follow_redirects = True)
        self.assertIn(b'log in', results.data)

    def test_get_login_200(self):
        """GET login route."""
        results = self.Client.get("/login")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'not registered', results.data)



class TestFlaskRouteLogIn(unittest.TestCase):

    def setUp(self):
        """Set up elements before every test."""
        self.Client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.Client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'liz@gmail.com'

        # connect to test database 
        connect_to_db(app, "postgresql:///testdb")

        # create tables and add sample data 
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at the end of every test."""

        db.session.close()
        db.drop_all()


    def test_post_login_200(self):
        """POST login form."""
        results = self.Client.post("/login",
                                    data = {"email": "test@test123.com",
                                            "password": "test"},
                                    follow_redirects=True)
        self.assertEqual(results.status_code, 200)

    def test_get_add_art_200(self):
        """GET add_art route."""
        results = self.Client.get("/add_art")
        self.assertEqual(results.status_code, 302)
        self.assertIn(b'title', results.data)

    def test_post_add_art_200(self):
        """POST add_art form."""
        results = self.Client.post("/add_art",
                                   data={
                                   "title": "testartwork",
                                   "artist": "testartist",
                                   "address": "657 Mission Street. San Francisco, CA 94105",
                                   "hint": "test_hint"
                                   })
        self.assertEqual(results.status_code, 302)

    # def test_post_add_art_invalid_400(self):
    #     """POST add_art invalid form."""
    #     results = self.Client.post("/add_art",
    #                                data={
    #                                "artist": "testartist",
    #                                "hint": "test_hint"
    #                                })
    #     self.assertEqual(results.status_code, 400)

    def test_get_profile_200(self):
        """non-database test for profile route."""
        results = self.Client.get('/profile')
        self.assertEqual(results.status_code, 302)


    def test_logout_200(self):
        """log user out"""
        pass 


if __name__ == '__main__':
    # runs tests if called like a script 
    import unittest
    unittest.main()
