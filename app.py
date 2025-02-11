from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Enable CORS for frontend
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow frontend access

# Define Database Path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "pharmacy.db")

# Get Database Connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables fetching results as dictionaries
    return conn

# Initialize Database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock yesno NOT NULL,
            expiry_date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Render Frontend
@app.route('/')
def home():
    return render_template('index.html')  # Ensure 'index.html' is in /templates/

# Add Medicine
@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        expiry_date = data.get('expiry_date')

        if not all([name, price, stock, expiry_date]):
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicines (name, price, stock, expiry_date) VALUES (?, ?, ?, ?)",
                       (name, price, stock, expiry_date))
        conn.commit()
        conn.close()

        return jsonify({"message": "Medicine added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Medicines
@app.route('/medicines', methods=['GET'])
def get_medicines():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, stock, expiry_date FROM medicines")
        medicines = cursor.fetchall()
        conn.close()

        # Convert to list of dictionaries for JSON response
        medicine_list = [{"id": row[0], "name": row[1], "price": row[2], "stock": row[3], "expiry_date": row[4]} for row in medicines]

        return jsonify({"medicines": medicine_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete Medicine
@app.route('/delete_medicine/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Medicine deleted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
