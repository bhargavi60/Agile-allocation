import mysql.connector
from config import DATABASE_CONFIG

class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.config = DATABASE_CONFIG
        print(self.config)

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Connected to the database")
            return self.connection
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None
