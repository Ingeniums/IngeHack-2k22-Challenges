import sqlite3
import os
from flask import Flask, jsonify, request, g, Response

app = Flask(__name__)
app.database = "challenge.db"
FLAG = os.getenv('FLAG', 'IngeHack{fake}')

def connect_db():
    return sqlite3.connect(app.database)

def init_db():
    with app.app_context():
        g.db = connect_db()
        g.db.execute("DROP TABLE IF EXISTS hero")
        g.db.execute("""CREATE TABLE IF NOT EXISTS hero (\n
        id INTEGER PRIMARY KEY AUTOINCREMENT,\n
        name TEXT UNIQUE NOT NULL,\n
        secret VARCHAR(32) NOT NULL)\n
        """)
        g.db.execute("DROP TABLE IF EXISTS feedbacks")
        g.db.execute("""CREATE TABLE IF NOT EXISTS feedbacks (\n
        id INTEGER PRIMARY KEY AUTOINCREMENT,\n
        feedback TEXT NOT NULL)\n
        """)
        g.db.execute(
            f"INSERT INTO hero (id, name, secret) VALUES (1, 'fa2y', '{FLAG}')")
        g.db.commit()
        g.db.close()


init_db()

@app.route('/')
def index():
    return jsonify({'success': 'post feedback'})

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        g.db = connect_db()
        feedback = request.form['feedback']
        if feedback:
            try:
                g.db.execute(f"INSERT INTO feedbacks (feedback) VALUES ('{feedback}')")
                g.db.commit()
            except Exception as e:
                return jsonify({'error': str(e)})
        g.db.close()
        return jsonify({'success': True})

    return jsonify({'success': False})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
