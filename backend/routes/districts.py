from flask import Blueprint, jsonify
from config import get_db_connection

districts_bp = Blueprint('districts', __name__)

@districts_bp.route('/', methods=['GET'])
def get_all_districts():
    conn = get_db_connection()
    districts = conn.execute("SELECT * FROM districts").fetchall()
    conn.close()
    return jsonify([dict(d) for d in districts])

@districts_bp.route('/<int:id>', methods=['GET'])
def get_district(id):
    conn = get_db_connection()
    district = conn.execute("SELECT * FROM districts WHERE id = ?", (id,)).fetchone()
    conn.close()
    if district:
        return jsonify(dict(district))
    return jsonify({"error": "District not found"}), 404

@districts_bp.route('/risk/<level>', methods=['GET'])
def get_by_risk(level):
    conn = get_db_connection()
    districts = conn.execute("SELECT * FROM districts WHERE risk_level = ?", (level,)).fetchall()
    conn.close()
    return jsonify([dict(d) for d in districts])