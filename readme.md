# Allsvenskan Stats

## Requirements
Make sure you have Docker and Python installed

## Getting started
1. `docker-compose up -d`
2. Ask [@ringish](https://www.github.com/ringish) for db backup & import with `docker cp database_backup.sql name-of-container:/database_backup.sql` and then `docker exec -t name of container psql -U user -d db -f /database_backup.sql`
3. `cd server`
4. `pip install -r requirements.txt`
5. `python app.py`