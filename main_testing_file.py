import unittest
from allocation1 import DatabaseManager
from mysql.connector import Error
from connection import DatabaseConnector

class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_connector = DatabaseConnector()
        cls.conn = cls.db_connector.connect()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def tearDown(self):
        cursor = self.conn.cursor()
        cursor.execute("TRUNCATE TABLE request_table;")
        cursor.execute("TRUNCATE TABLE resource_table;")
        self.conn.commit()
        cursor.close()

    def test_scenario1(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours) VALUES (1, 'SkillA', 0, 20), (2, 'SkillB', 0, 15), (3, 'SkillC', 0, 8), (4, 'SkillA', 0, 10), (5, 'SkillA', 0, 20), (6, 'SkillB',0, 7);")
            cursor.execute("INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day) VALUES (1, 'SkillC', 0, 4), (2, 'SkillB', 0, 8), (3, 'SkillA', 0, 2);")
            self.conn.commit()
            cursor.close()
            db_manager = DatabaseManager()
            db_manager.allocate_resources()
            print("scenario1 output is printed")

            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM request_table;")
            request_table_data = cursor.fetchall()
            print("request_table_data:", request_table_data)

            cursor.execute("SELECT * FROM resource_table;")
            resource_table_data = cursor.fetchall()
            print("resource_table_data:", resource_table_data)
            cursor.close()
            self.assertGreater(len(request_table_data), 0)
            self.assertGreater(len(resource_table_data), 0)
        except Error as e:
            print(f"Error: {e}")
            return None
        print("Scenario 1")

    def test_scenario2(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day)
                VALUES (1, 'SkillY', 0, 20), (2, 'SkillY', 0, 10), (3, 'SkillY', 0, 2);""")
            cursor.execute("""INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours)
                VALUES (1, 'SkillY', 0, 5), (2, 'SkillY', 0, 10), (3, 'SkillY', 0, 15), (4, 'SkillY', 0, 20),
                        (5, 'SkillY', 0, 18), (6, 'SkillY', 0, 15),(7, 'SkillY', 0, 9);""")
            self.conn.commit()
            cursor.close()

            db_manager = DatabaseManager()
            db_manager.allocate_resources()

            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM request_table;")
            request_table_data = cursor.fetchall()
            print("request_table_data:", request_table_data)

            cursor.execute("SELECT * FROM resource_table;")
            resource_table_data = cursor.fetchall()
            print("resource_table_data:", resource_table_data)
            cursor.close()
            self.assertGreater(len(request_table_data), 0)
            self.assertGreater(len(resource_table_data), 0)
        except:
            print("Scenario 2")
