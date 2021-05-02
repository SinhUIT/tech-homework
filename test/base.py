import unittest
from src.api import app


class BaseTestCase(unittest.TestCase):
    """ Base Tests """
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

