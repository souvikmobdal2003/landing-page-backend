from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Create table
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            appType TEXT,
            launchTimeline TEXT,
            budgetRange TEXT
        )''')
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')  # Looks in templates/index.html

# Submit form data (POST)
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print("Received:", data)  # For debugging

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO leads (name, email, phone, appType, launchTimeline, budgetRange) VALUES (?, ?, ?, ?, ?, ?)',
                  (data['name'], data['email'], data['phone'], data['appType'], data['launchTimeline'], data['budgetRange']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

# ✅ New Route to Get All Leads (GET)
@app.route('/api/leads', methods=['GET'])
def get_leads():
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # So column names are preserved
        c = conn.cursor()
        c.execute('SELECT * FROM leads')
        rows = c.fetchall()
        leads = [dict(row) for row in rows]  # Convert rows to list of dicts
        conn.close()
        return jsonify(leads), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
