from datetime import datetime, timedelta
import pandas as pd
from connection import DatabaseConnector
from config import SPECIFIED_DATE
from workalendar.usa import UnitedStates

class DatabaseManager:
    def __init__(self):
        self.start_date = SPECIFIED_DATE
        self.changed_date = None
    def create_db_connection(self):
        db_connector = DatabaseConnector()
        return db_connector.connect()

    def allocate_resources(self):
        conn = self.create_db_connection()
        if conn is not None:
            try:
                db_cursor = conn.cursor()
                db_cursor.execute('SELECT * FROM `test_db`.`request_table` WHERE resource_id = 0;')
                table_data1 = db_cursor.fetchall()
                column_names1 = [i[0] for i in db_cursor.description]
                request_table = pd.DataFrame(table_data1, columns=column_names1)
                
                db_cursor.execute('SELECT * FROM `test_db`.`resource_table` WHERE capacity_in_hours_per_day > 0;')
                table_data2 = db_cursor.fetchall()
                column_names2 = [i[0] for i in db_cursor.description]
                resource_table = pd.DataFrame(table_data2, columns=column_names2)
                
                request_table['start_date'] = None
                request_table['end_date'] = None
                print(request_table)
                print(resource_table)
                cal = UnitedStates()

                holidays = cal.holidays(2023)
                print(holidays)

                for _, request in request_table.iterrows():
                    matching_resources = resource_table[resource_table['res_skill'] == request['req_skill']]
                    if not matching_resources.empty:
                        matching_resources['allocation'] = matching_resources['allocation_hours'] / matching_resources['capacity_in_hours_per_day']
                        sorted_resources = matching_resources.sort_values(by=['allocation'])
                        print(matching_resources)
                        min_allocated_resource = sorted_resources.iloc[0]
                        resource_id = min_allocated_resource['res_id']
                        request_id = request['req_id']
                        allocation_hours = request['efforts_in_hours']

                        previous_assignment = request_table[request_table['resource_id'] == resource_id]
                        print(previous_assignment)
                        days_to_complete = allocation_hours / min_allocated_resource['capacity_in_hours_per_day']
                        if not previous_assignment.empty:
                            previous_request_id = previous_assignment.iloc[-1]['req_id']
                            previous_assignment_end_date = request_table[request_table['req_id'] == previous_request_id]['end_date'].values[0]
                            print(previous_assignment_end_date)
                            if previous_assignment_end_date:
                                self.changed_date = datetime.strptime(previous_assignment_end_date, '%Y-%m-%d').date() + timedelta(days=1)
                                print(self.changed_date)
                        else:
                            self.changed_date = self.start_date

                        end_date = self.get_end_date(self.changed_date, days_to_complete, holidays)
                        print(end_date)
                        request_table.loc[request_table['req_id'] == request_id, 'start_date'] = self.changed_date
                        request_table.loc[request_table['req_id'] == request_id, 'end_date'] = end_date

                        resource_table.loc[resource_table['res_id'] == resource_id, 'allocation_hours'] += allocation_hours
                        request_table.loc[request_table['req_id'] == request_id, 'resource_id'] = resource_id
                        update_query1 = f"UPDATE request_table SET resource_id = {resource_id}, start_date = '{self.changed_date}', end_date = '{end_date}' WHERE req_id = {request_id}"
                        db_cursor.execute(update_query1)
                        update_query2 = f"UPDATE resource_table SET allocation_hours = allocation_hours + {allocation_hours} WHERE res_id = {resource_id}"
                        db_cursor.execute(update_query2)

                print(request_table)
                print(resource_table)
                conn.commit()
                conn.close()
                print("Allocations completed and saved to the database.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Database connection failed")

    def get_end_date(self, changed_date, days_to_complete, holidays):
        if isinstance(changed_date, str): 
            current_date = datetime.strptime(str(changed_date), '%Y-%m-%d')
        else:
            current_date = changed_date
        print(current_date)
        if days_to_complete <= 1:
            return current_date.strftime('%Y-%m-%d')
        while days_to_complete > 0:
            current_date += timedelta(days=1) 
            if current_date.weekday() < 5 and current_date.strftime('%Y-%m-%d') not in holidays:
                days_to_complete -= 1
        return current_date.strftime('%Y-%m-%d')

