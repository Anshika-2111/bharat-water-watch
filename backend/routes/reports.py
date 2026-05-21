from flask import Blueprint, jsonify, request
from config import get_db_connection

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
def get_all_reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, d.name as district_name, d.state 
        FROM reports r 
        JOIN districts d ON r.district_id = d.id
        ORDER BY r.created_at DESC
    """)
    reports = cursor.fetchall()
    cursor.close()
    conn.close()
    for r in reports:
        r['created_at'] = str(r['created_at'])
    return jsonify(reports)

@reports_bp.route('/', methods=['POST'])
def submit_report():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (district_id, issue_type, description, reported_by)
        VALUES (%s, %s, %s, %s)
    """, (
        data['district_id'],
        data['issue_type'],
        data['description'],
        data.get('reported_by', 'Anonymous')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Report submitted successfully! ✅"}), 201

@reports_bp.route('/<int:id>/status', methods=['PATCH'])
def update_status(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET status = %s WHERE id = %s", (data['status'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Status updated! ✅"})
