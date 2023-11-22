import psycopg2
import psycopg2.extras
from config import db_params

class MatchRepository:
    def get_matches(self, year=None, match_round=None):
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Base query
        query = """
            SELECT m.match_id, ht.team_name AS home_team_name, at.team_name AS away_team_name,
                m.home_team_score, m.away_team_score, m.match_date, m.match_time,
                m.season, m.match_round
            FROM matches m
            JOIN teams ht ON m.home_team_id = ht.team_id
            JOIN teams at ON m.away_team_id = at.team_id
        """

        # Filter conditions
        conditions = []
        params = []

        if year:
            conditions.append("EXTRACT(YEAR FROM m.match_date) = %s")
            params.append(year)

        if match_round:
            conditions.append("m.match_round = %s")
            params.append(match_round)

        # Append conditions to the query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        cursor.execute(query, tuple(params))
        matches = cursor.fetchall()

        cursor.close()
        conn.close()

        return matches

    def get_match_details(self, match_id):
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Fetch match details including team names and IDs
        cursor.execute("""
        SELECT m.match_date, m.match_time, m.season, m.match_round, m.visitors,
            ht.team_name as home_team_name, ht.team_id as home_team_id,
            at.team_name as away_team_name, at.team_id as away_team_id,
            m.home_team_score, m.away_team_score, s.stadium_name,
            array_agg(r.referee_name) FILTER (WHERE mr.role = 'Main Referee') as main_referee,
            array_agg(r.referee_name) FILTER (WHERE mr.role LIKE 'Assistant Referee') as assistant_referees,
            array_agg(r.referee_name) FILTER (WHERE mr.role = 'Fourth Official') as fourth_official
            FROM matches m
            JOIN teams ht ON m.home_team_id = ht.team_id
            JOIN teams at ON m.away_team_id = at.team_id
            LEFT JOIN stadiums s ON m.stadium_id = s.stadium_id
            LEFT JOIN match_referees mr ON m.match_id = mr.match_id
            LEFT JOIN referees r ON mr.referee_id = r.referee_id
            WHERE m.match_id = %s
            GROUP BY m.match_date, m.match_time, m.season, m.match_round, m.visitors,
                    ht.team_name, ht.team_id, at.team_name, at.team_id,
                    m.home_team_score, m.away_team_score, s.stadium_name
        """, (match_id,))
        match = cursor.fetchone()
        
        cursor.close()
        conn.close()

        return match
