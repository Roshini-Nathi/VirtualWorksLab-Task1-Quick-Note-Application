from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Add Note
@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()

    note = data.get('note')

    if not note:
        return jsonify({"error": "Note cannot be empty"}), 400

    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved successfully"})


# Get All Notes
@app.route('/get_notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, content FROM notes ORDER BY id DESC"
    )

    notes = cursor.fetchall()

    conn.close()

    notes_list = []

    for note in notes:
        notes_list.append({
            "id": note[0],
            "content": note[1]
        })

    return jsonify(notes_list)


# Run Application
if __name__ == '__main__':
    app.run(debug=True)