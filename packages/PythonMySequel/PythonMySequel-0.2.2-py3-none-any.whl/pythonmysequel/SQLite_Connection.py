'''
A class for connecting to SQLite, instead of MySQL
as well as interacting with the database
(eg. creating tables, inserting into tables, etc)
'''

from .Connection import Connection
import sqlite3

class SQLite_Connection(Connection):
    def __init__(self, database:str) -> None:
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    def _execute(self, execute_string:str, execute_data:list=[]):
        if execute_data:
            self.cursor.execute(execute_string.replace('%s', '?'), execute_data)
            self.last_query = (execute_string % tuple(execute_data))
        else:
            self.cursor.execute(execute_string)
            self.last_query = execute_string
        self.connection.commit()