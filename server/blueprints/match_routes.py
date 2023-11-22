from flask import Blueprint, jsonify, request
from services.match_service import MatchService

match_blueprint = Blueprint('match_blueprint', __name__)

@match_blueprint.route('/matches/<int:year>', methods=['GET'])
@match_blueprint.route('/matches/<int:year>/<int:round>', methods=['GET'])
def get_matches(year, round=None):
    match_service = MatchService()
    matches = match_service.get_matches(year, round)
    if not matches:
        return jsonify({'error': 'No matches found'}), 404
    return jsonify(matches)

@match_blueprint.route('/match/<int:match_id>', defaults={'details': None}, methods=['GET'])
@match_blueprint.route('/match/<int:match_id>/<details>', methods=['GET'])
def get_match(match_id, details):
    match_service = MatchService()
    match_details = match_service.get_match(match_id, details)
    if not match_details:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify(match_details)