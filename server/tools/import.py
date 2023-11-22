import json
import psycopg2
from app.config import db_params

# List of tables to import
tables = [
    'player_team_link',
    'players',
    'referees',
    'match_referees',
    'stadiums',
    'teams',
    'matches',
    'match_events'
]

def import_json_data(table_name, cursor):
    # Open the JSON file for the table
    with open(f'./data/{table_name}.json', 'r') as infile:
        data = json.load(infile)
    
    # Clear existing data in the table (be cautious with this in a production environment)
    cursor.execute(f"DELETE FROM {table_name}")
    
    # Insert new data into the table
    for record in data:
        columns = ', '.join(record.keys())
        placeholders = ', '.join(['%s'] * len(record))
        values = tuple(record.values())
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Import data for each table
for table in tables:
    import_json_data(table, cursor)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()