from flask import Blueprint, jsonify, request
from config import get_db_connection

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    conn = get_db_connection()
    reports = conn.execute('''
        SELECT r.*, d.name as district_name, d.state
        FROM reports r
        JOIN districts d ON r.district_id = d.id
        ORDER BY r.created_at DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in reports])

@reports_bp.route('/', methods=['POST'])
def submit_report():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO reports (district_id, issue_type, description, reported_by)
        VALUES (?, ?, ?, ?)
    ''', (
        data['district_id'],
        data['issue_type'],
        data['description'],
        data.get('reported_by', 'Anonymous')
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Report submitted successfully! ✅"}), 201

@reports_bp.route('/<int:id>/status', methods=['PATCH'])
def update_status(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute("UPDATE reports SET status = ? WHERE id = ?", (data['status'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Status updated! ✅"})