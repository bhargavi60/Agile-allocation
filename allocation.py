import pandas as pd
from connection import DatabaseConnector

class DatabaseManager:
    def create_db_connection(self):
        db_connector = DatabaseConnector()
        return db_connector.connect()
    
    def allocate_resources(self):
        conn = self.create_db_connection()
        if conn is not None:
            try:
                db_cursor = conn.cursor()
                db_cursor.execute('SELECT * FROM `test_db`.`request_table`;')
                table_data1 = db_cursor.fetchall()
                column_names1 = [i[0] for i in db_cursor.description]
                request_table = pd.DataFrame(table_data1, columns=column_names1)
                db_cursor.execute('SELECT * FROM `test_db`.`resource_table`;')
                table_data2 = db_cursor.fetchall()
                column_names2 = [i[0] for i in db_cursor.description]
                sample_df = pd.DataFrame(table_data2, columns=column_names2)
                resource_table = sample_df[sample_df['capacity_in_hours_per_day'] > 0]
                
                for _, request in request_table.iterrows():
                    matching_resources = resource_table[resource_table['res_skill'] == request['req_skill']]
                    if not matching_resources.empty:
                        matching_resources['allocation'] = matching_resources['allocation_hours'] / matching_resources['capacity_in_hours_per_day']
                        sorted_resources = matching_resources.sort_values(by=['allocation'])
                        min_allocated_resource = sorted_resources.iloc[0]
                        resource_id = min_allocated_resource['res_id']
                        request_id = request['req_id']
                        allocation_hours = request['efforts_in_hours']                    
                        resource_table.loc[resource_table['res_id'] == resource_id, 'allocation_hours'] += allocation_hours
                        request_table.loc[request_table['req_id'] == request_id, 'resource_id'] = resource_id

                        update_query1 = f"UPDATE request_table SET resource_id = {resource_id} WHERE req_id = {request_id}"
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
            print("Database connection failed.")


            