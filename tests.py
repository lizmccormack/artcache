import unittest
from server import app 
import googlemaps
import os


class TestFlaskRoutesNoLogIn(unittest.TestCase):

    def setUp(self):
        """Set up elements before every test."""
        self.Client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


    def test_get_homepage(self):
        """non-database test for home route."""
        results = self.Client.get("/")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Map</h1>', results.data)


    def test_get_register(self):
        """non-database test for register route."""
        results = self.Client.get("/register")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Register!</h1>', results.data)

    def test_post_login(self):
        """non-database test for POST register form."""
        results = self.Client.post("/register",
                                   data = {"email": "test@test123.com",
                                           "username": "test user",
                                           "password": "test"},
                                    follow_redirects = True)
        self.assertEqual(results.status_code, 200)



    def test_get_login(self):
        """non-database test for login route."""
        results = self.Client.get("/login")
        self.assertEqual(results.status_code, 200)
        self.assertIn(b'<h1>Login</h1>', results.data)

    def test_post_login(self):
        """non-database test for POST login form."""
        results = self.Client.post("/login",
                                    data = {"email": "test@test123.com",
                                            "password": "test"},
                                    follow_redirects=True)
        self.assertEqual(results.status_code, 200)


# class TestFlaskRouteLogIn(unittest.TestCase):

#     def setUp(self):

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         self.client = app.test_client()

#         with self.client as c: 
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_add_art(self):
#         """non-database test for add_art route."""
#         results = self.client.get("/add_art")
#         self.assertEqual(results.status_code, 200)
#         self.assertIn(b'<h1>Add Art Site</h1>', results.data)


#     def test_profile(self):
#         """non-database test for profile route."""
#         results = self.client.get('/profile')
#         self.assertEqual(results.status_code, 200)


  

# test cases 
# - user already registered, goes to login route w/ flash message saying already registered 
# - user registers for the first time, goes to login route w/ flash message saying thanks for registering 

# test cases 
# - user in userdb, login and go to homepage 
# - user not in db because go back to login 



if __name__ == '__main__':
    # runs tests if called like a script 
    unittest.main()
