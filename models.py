import os
import json
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
local_database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

database_path = os.environ.get('DATABASE_URL', local_database_path)

db = SQLAlchemy()

'''
setup_db(app)
	binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
	app.config["SQLALCHEMY_DATABASE_URI"] = database_path
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)
	db.create_all()


'''
Person
Have title and release year
'''
class Person(db.Model):  
	__tablename__ = 'People'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	catchphrase = Column(String)

	def __init__(self, name, catchphrase=""):
		self.name = name
		self.catchphrase = catchphrase

	def format(self):
		return {
			'id': self.id,
			'name': self.name,
			'catchphrase': self.catchphrase}