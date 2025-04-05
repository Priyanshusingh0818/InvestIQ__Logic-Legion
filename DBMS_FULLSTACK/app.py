from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Warsha@1980'
app.config['MYSQL_DB'] = 'StockApp'

# Database connection
db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def home():
    # Render the login page as the default route
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    name = data['name']
    email = data['email']
    age = data['age']
    gender = data['gender']
    password = data['password']

    try:
        cursor = db.cursor()
        query = """
            INSERT INTO users (name, email, age, gender, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, age, gender, password))
        db.commit()
        return redirect(url_for('home'))  # Redirect to the login page after successful registration
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)})

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data['email']
    password = data['password']

    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"message": "Login successful!", "user": user})  # Modify this as per your requirement
        else:
            return jsonify({"error": "Invalid email or password."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Replace 5001 with your desired port number
