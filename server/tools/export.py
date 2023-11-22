import psycopg2
import json
from app.config import db_params

tables = [
    'players',
    'referees',
    'match_referees',
    'player_team_link',
    'stadiums',
    'teams',
    'matches',
    'match_referees',
    'match_events'
    ]

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
for table in tables:
    # Query to select all data from a table
    cursor.execute(f"SELECT json_agg(t) FROM (SELECT * FROM {table}) t")
    result = cursor.fetchone()[0]

    # Write the result to a file
    with open(f'./data/{table}.json', 'w') as outfile:
        json.dump(result, outfile, indent=2)

cursor.close()
conn.close()