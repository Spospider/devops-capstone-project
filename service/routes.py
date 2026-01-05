"""
Flask routes for the service.
This module relaxes the Content-Type check for JSON requests so tests (and clients)
that omit or vary the Content-Type header are handled more gracefully.
"""
from flask import Blueprint, request, jsonify
import json

bp = Blueprint('service', __name__)


def _is_json_content_type():
    """Return True when the request's Content-Type indicates JSON.

    This is a relaxed check: it returns True if the Content-Type header is
    missing but the body can be parsed as JSON, or if the header contains the
    substring 'json' (to allow values like 'application/json; charset=utf-8').
    """
    content_type = request.headers.get('Content-Type', '')

    if content_type:
        # Accept any content-type that includes 'json' (case-insensitive)
        if 'json' in content_type.lower():
            return True
        return False

    # No Content-Type header: try to parse the body to see if it's JSON
    try:
        raw = request.get_data(cache=True)
        if not raw:
            return False
        # Try to decode and parse as JSON. If it fails, it's not JSON.
        json.loads(raw.decode('utf-8'))
        return True
    except Exception:
        return False


@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@bp.route('/predict', methods=['POST'])
def predict():
    # Relaxed content-type validation
    if not _is_json_content_type():
        return jsonify({'error': 'Request must be JSON (Content-Type application/json)'}), 400

    # Parse JSON payload; use silent=True to avoid raising a BadRequest
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    # Example processing - replace with actual logic
    # For tests, simply echo back the payload with a success flag
    return jsonify({'success': True, 'input': data})
