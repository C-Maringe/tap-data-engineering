import mysql.connector
from datetime import datetime

startTime = datetime.now()
print(f'start time: {startTime}')

source_db_config = {
    'host': '',
    'port': '',
    'user': '',
    'password': '',
    'database': ''
}

local_db_config = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'root',
    'database': 'local_tap'
}

print("Initializing source database connection...")
source_connection = mysql.connector.connect(**source_db_config)
source_cursor = source_connection.cursor()
print("Source database connected...")

print("Initializing local database connection...")
local_connection = mysql.connector.connect(**local_db_config)
local_cursor = local_connection.cursor()
print("Local database connected...")

table_name = 'card'

print("Extracting column info from server db...")
source_cursor.execute(f"SHOW COLUMNS FROM {table_name}")
columns_info = source_cursor.fetchall()

print("getting columns names and datatypes")
columns = [column_info[0] for column_info in columns_info]
data_types = [column_info[1] for column_info in columns_info]

print("creating table on local")
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{column} {data_type}' for column, data_type in zip(columns, data_types)])})"
local_cursor.execute(create_table_query)

print("executing select *...")
source_cursor.execute(f'SELECT * FROM {table_name}')
print("Fetching data...")
data_to_insert = source_cursor.fetchall()

print("Data fetch finished...")
for index, row in enumerate(data_to_insert, 1):
    print(f'Inserting row number {index}')
    insert_query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(columns))})'
    local_cursor.execute(insert_query, row)

local_connection.commit()
local_cursor.close()
local_connection.close()

source_cursor.close()
source_connection.close()

endTime = datetime.now()
print(f'End time: {endTime}')
print(f'Time taken: {endTime - startTime}')
