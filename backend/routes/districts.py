from flask import Blueprint, jsonify
from config import get_db_connection

districts_bp = Blueprint('districts', __name__)

@districts_bp.route('/', methods=['GET'])
def get_all_districts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM districts")
    districts = cursor.fetchall()
    cursor.close()
    conn.close()
    for d in districts:
        d['last_updated'] = str(d['last_updated'])
    return jsonify(districts)

@districts_bp.route('/<int:id>', methods=['GET'])
def get_district(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM districts WHERE id = %s", (id,))
    district = cursor.fetchone()
    cursor.close()
    conn.close()
    if district:
        district['last_updated'] = str(district['last_updated'])
        return jsonify(district)
    return jsonify({"error": "District not found"}), 404

@districts_bp.route('/risk/<level>', methods=['GET'])
def get_by_risk(level):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM districts WHERE risk_level = %s", (level,))
    districts = cursor.fetchall()
    cursor.close()
    conn.close()
    for d in districts:
        d['last_updated'] = str(d['last_updated'])
    return jsonify(districts)