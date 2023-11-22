from repositories.match_repository import MatchRepository
from repositories.player_repository import PlayerRepository
from repositories.event_repository import EventRepository

class MatchService:
    def __init__(self):
        self.match_repo = MatchRepository()
        self.player_repo = PlayerRepository()
        self.event_repo = EventRepository()
    
    def get_matches(self, year, round=None):
        matches_response = self.match_repo.get_matches(year, round)

        matches = [
            {
                'match_id': match['match_id'],
                'home_team': match['home_team_name'],
                'away_team': match['away_team_name'],
                'home_score': match['home_team_score'],
                'away_score': match['away_team_score'],
                'match_date': match['match_date'].isoformat(),
                'match_time': match['match_time'].strftime('%H:%M:%S') if match['match_time'] else None,
                'season': match['season'],
                'round': match['match_round']
            } for match in matches_response
        ]
        return matches

    def get_match(self, match_id, events=None):
        match_response = self.match_repo.get_match_details(match_id)
        starting_players = self.player_repo.get_starting_players(match_id)
        home_squad = [player[0] for player in starting_players if player[1] == match_response['home_team_id']]
        away_squad = [player[0] for player in starting_players if player[1] == match_response['away_team_id']]
        match_time = match_response['match_time'].strftime('%H:%M:%S') if match_response['match_time'] else None
        match = {
            'match_date': match_response[0],
            'match_time': match_time,
            'season': match_response[2],
            'round': match_response[3],
            'home_team': match_response['home_team_name'],
            'away_team': match_response['away_team_name'],
            'home_team_score': match_response['home_team_score'],
            'away_team_score': match_response['away_team_score'],
            'home_squad': home_squad,
            'away_squad': away_squad,
            'stadium': match_response['stadium_name'],
            'referee': match_response['main_referee'],
            'assistant_referees': match_response['assistant_referees'],
            'fourth_official': match_response['fourth_official'],
            'visitors': match_response['visitors']
        }
        if events:
            events_response = self.event_repo.get_match_events(match_id)
            events = [
                {
                    'player': event['player_name'],
                    'event_type': event['event_type'],
                    'event_minute': event['event_minute'],
                    'team_id': event['team_id']
                } for event in events_response
            ]
            match['events'] = events
        
        return match