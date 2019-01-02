import sqlite3



class SQLighter:

	def __init__(self, database):
		self.connect = sqlite3.connect(database)
		self.cursor = self.connection.cursor()
