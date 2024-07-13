import unittest
from allocation1 import DatabaseManager
from mysql.connector import Error
from connection import DatabaseConnector

class BaseDatabaseManagerTestCase():
    @classmethod
    def setUpClass(cls):
        cls.db_connector = DatabaseConnector()
        cls.conn = cls.db_connector.connect()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        cursor = self.conn.cursor()
        cursor.execute("TRUNCATE TABLE request_table;")
        cursor.execute("TRUNCATE TABLE resource_table;")
        self.conn.commit()
        cursor.close()

    def run_scenario(self):
        raise NotImplementedError("Subclasses must implement run_scenario")

class Scenario1TestCase(BaseDatabaseManagerTestCase,unittest.TestCase):
    def test_scenario1(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours) VALUES (1, 'SkillA', 0, 20), (2, 'SkillB', 0, 15), (3, 'SkillC', 0, 8), (4, 'SkillA', 0, 10), (5, 'SkillA', 0, 20), (6, 'SkillB',0, 7);")
            cursor.execute("INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day) VALUES (1, 'SkillC', 0, 4), (2, 'SkillB', 0, 8), (3, 'SkillA', 0, 2);")
            self.conn.commit()
            cursor.close()
            cursor = self.conn.close()
            db_manager = DatabaseManager()
            db_manager.allocate_resources()
            print("Scenario 1")
        except Error as e:
            print(f"Error: {e}")
            return None

class Scenario2TestCase(BaseDatabaseManagerTestCase, unittest.TestCase):
    def test_scenario2(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day) VALUES (1, 'SkillY', 0, 20), (2, 'SkillY', 0, 10), (3, 'SkillY', 0, 2);")
            cursor.execute("INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours) VALUES (1, 'SkillY', 0, 5), (2, 'SkillY', 0, 10), (3, 'SkillY', 0, 15), (4, 'SkillY', 0, 20),(5, 'SkillY', 0, 18), (6, 'SkillY', 0, 15),(7, 'SkillY', 0, 9);")
            self.conn.commit()
            cursor.close()
            cursor = self.conn.close()
            db_manager = DatabaseManager()
            db_manager.allocate_resources()
            print("Scenario 2")
        except Error as e:
            print(f"Error: {e}")
            return None
   
class Scenario3TestCase(BaseDatabaseManagerTestCase,unittest.TestCase):
    def test_scenario3(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day)
                VALUES (1, 'SkillX', 0, 0), (2, 'SkillY', 0, 10), (3, 'SkillZ', 0, 20),(4, 'SkillZ', 0, 0),(5, 'SkillX', 0, 10);""")
            cursor.execute("""INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours)
                VALUES (1, 'SkillX', 0, 10), (2, 'SkillY', 0, 30),(3, 'SkillX', 0, 15), (4, 'SkillY', 0, 10),(5, 'SkillZ', 0, 18);""")
            self.conn.commit()
            cursor.close()
            cursor = self.conn.close()
            db_manager = DatabaseManager()
            db_manager.allocate_resources()
            print("Scenario 3")
        except Error as e:
            print(f"Error: {e}")
            return None
        
class Scenario4TestCase(BaseDatabaseManagerTestCase,unittest.TestCase):
    def test_scenario4(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""INSERT INTO resource_table (res_id, res_skill, allocation_hours, capacity_in_hours_per_day)
                VALUES (1, 'SkillX', 0, 5), (2, 'SkillX', 0, 10),(5, 'SkillX', 0, 10);""")
            cursor.execute("""INSERT INTO request_table (req_id, req_skill, resource_id, efforts_in_hours)
                VALUES (1, 'SkillX', 0, 100), (2, 'SkillX', 0, 30),(3, 'SkillX', 0, 15), (4, 'SkillX', 0, 10),(5, 'SkillX', 0, 18) ;""")
            self.conn.commit()
            cursor.close()
            cursor = self.conn.close()
            db_manager = DatabaseManager()
            db_manager.allocate_resources()
            print("Scenario 4")
        except Error as e:
            print(f"Error: {e}")
            return None