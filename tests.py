from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
	def setUp(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u = User(username='test_1')
		u.set_password('correct_pw')
		self.assertFalse(u.check_password('wrong_pw'))
		self.assertTrue(u.check_password('correct_pw'))


if __name__ == '__main__':
	unittest.main(verbosity=2)