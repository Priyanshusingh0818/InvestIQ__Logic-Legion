from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Warsha@1980',  # Replace with your MySQL password
    'database': 'stockapp'
}

# Function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Serve the main HTML page
@app.route('/')
def index():
    return render_template('quiz.html')

# API endpoint to submit quiz score
@app.route('/submit_score', methods=['POST'])
def submit_score():
    try:
        # Get score from request
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            return jsonify({'error': 'Score is required'}), 400
        
        # Current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Connect to the database
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Insert the score into the database
        query = "INSERT INTO user_quizzes (quiz_score, quiz_timestamp) VALUES (%s, %s)"
        values = (score, timestamp)
        
        cursor.execute(query, values)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'message': 'Score saved successfully'}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Get all scores (admin endpoint)
@app.route('/scores', methods=['GET'])
def get_scores():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Get all scores ordered by timestamp (newest first)
        query = "SELECT * FROM user_quizzes ORDER BY quiz_timestamp DESC"
        cursor.execute(query)
        
        scores = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'scores': scores}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Get statistics about scores
@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        
        # Get statistics about scores
        queries = {
            'avg_score': "SELECT AVG(quiz_score) as avg_score FROM user_quizzes",
            'max_score': "SELECT MAX(quiz_score) as max_score FROM user_quizzes",
            'min_score': "SELECT MIN(quiz_score) as min_score FROM user_quizzes",
            'total_quizzes': "SELECT COUNT(*) as total_quizzes FROM user_quizzes",
            'recent_scores': "SELECT quiz_score, quiz_timestamp FROM user_quizzes ORDER BY quiz_timestamp DESC LIMIT 5"
        }
        
        stats = {}
        
        for key, query in queries.items():
            cursor.execute(query)
            if key != 'recent_scores':
                result = cursor.fetchone()
                stats[key] = result
            else:
                result = cursor.fetchall()
                stats[key] = result
        
        cursor.close()
        connection.close()
        
        return jsonify({'success': True, 'stats': stats}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Initialize the database if needed
def init_db():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_quizzes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                quiz_score INT NOT NULL,
                quiz_timestamp DATETIME NOT NULL
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("Database initialized successfully")
    
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

# Serve the HTML file from the static directory
@app.route('/')
def serve_quiz():
    return render_template('quiz.html')

# For static files
@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)
if __name__ == '__main__':
    app.run(debug=True, port=5003)