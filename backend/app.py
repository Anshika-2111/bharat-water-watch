from flask import Flask
from flask_cors import CORS
from routes.districts import districts_bp
from routes.reports import reports_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(districts_bp, url_prefix='/api/districts')
app.register_blueprint(reports_bp, url_prefix='/api/reports')

@app.route('/')
def home():
    return {"message": "Bharat Water Watch API is running! 💧"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)