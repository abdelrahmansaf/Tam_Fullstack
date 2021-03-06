import unittest
from app import app

class TestApiFlask(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()
        self.app.testing = True 


    def test_home_status_code(self):
        """ def status_code test if path is ok "/"
        """
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 200) 
        # ".status_code = renvoie, si marche = 200 (ok)


    def test_home_type(self):
        """ test_home_type test if te app is j.son content
        """
        result = self.app.get('/')
        self.assertTrue(result.data,'Hello')

    def test_stations(self):
        """ test_home_type test if te app is j.son content
        """
        result = self.app.get('/stations')
        self.assertTrue(b'Ligne'in result.data)
        self.assertFalse(b'Bonjour'in result.data)
    

    def test_home_by_country(self):
        result = self.app.get('/next/JACOU') 
        self.assertTrue(b'Station'in result.data)
        self.assertFalse(b'nothing'in result.data)
        


    def test_home_by_country(self):
        result = self.app.get('/next/<line>/<station>/<direction>') 
        self.assertTrue(b'Station'in result.data)
        self.assertFalse(b'nothing'in result.data)



if __name__ == '__main__':
    unittest.main()

