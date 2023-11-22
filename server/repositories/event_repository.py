import psycopg2
import psycopg2.extras
from config import db_params

class EventRepository:
    def get_match_events(self, match_id):
         # Get the starting squad for both teams
         # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT DISTINCT p.player_name, me.event_type, me.event_minute, ptl.team_id
            FROM match_events me
            JOIN players p ON me.player_id = p.player_id
            JOIN player_team_link ptl ON p.player_id = ptl.player_id
            WHERE me.match_id = %s AND me.event_type = 'EnteredPitch' AND me.event_minute IS NOT NULL
            ORDER BY me.event_minute
        """, (match_id,))
        events = cursor.fetchall()

        cursor.close()
        conn.close()

        return events