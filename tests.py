import unittest
from model import User, Artwork, Add, Log, connect_to_db, db
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
        # example_data()

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
        self.assertIn(b'<h1>Register!</h1>', results.data)

    def test_post_register_200(self):
        """POST registration form."""
        results = self.Client.post("/register",
                                   data = {"email": "test@test123.com",
                                           "username": "test user",
                                           "password": "test"},
                                    follow_redirects = True)
        self.assertEqual(results.status_code, 200)

    # def test_post_register_invalid_400(self):
    #     """POST an invalid registration form.
        
    #     user already exists in users table. 
    #     """
    #     results = self.Client.post("/register",
    #                                data = {"email": "test@test123.com",
    #                                        "username": "test user",
    #                                        "password": "test"},
    #                                 follow_redirects = True)
    #     self.assertEqual(results.status_code, 400)

    def test_get_login_200(self):
        """GET login route."""
        results = self.Client.get("/login")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Login</h1>', results.data)



class TestFlaskRouteLogIn(unittest.TestCase):

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


    def test_post_login_200(self):
        """POST login form."""
        results = self.Client.post("/login",
                                    data = {"email": "test@test123.com",
                                            "password": "test"},
                                    follow_redirects=True)
        self.assertEqual(results.status_code, 200)

    def test_get_add_art_200(self):
        """GET add_art route."""
        results = self.client.get("/add_art")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Add Art Site</h1>', results.data)

    def test_post_add_art_200(self):
        """POST add_art form."""
        pass

    def test_post_add_art_invalid_400(self):
        """POST add_art invalid form."""
        pass

    def test_get_profile_200(self):
        """non-database test for profile route."""
        results = self.client.get('/profile')
        self.assertEqual(results.status_code, 200)


    def test_logout_200(self):
        """log user out"""
        pass 


if __name__ == '__main__':
    # runs tests if called like a script 
    import unittest
    unittest.main()
