from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__) # <-- YE SABSE PEHLE HONA CHAHIYE
NOTES_FILE = 'notes.txt'

# Notes load karne ka function
def load_notes():
    notes = []
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(':', 1)
                    notes.append({'id': int(parts[0]), 'text': parts[1]})
    return notes

# Notes save karne ka function
def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        for note in notes:
            f.write(f"{note['id']}:{note['text']}\n")

# Website wale routes
@app.route('/')
def home():
    notes = load_notes()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    notes = load_notes()
    new_id = notes[-1]['id'] + 1 if notes else 1
    note_text = request.form['note']
    notes.append({'id': new_id, 'text': note_text})
    save_notes(notes)
    return redirect(url_for('home'))

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    notes = load_notes()
    notes = [note for note in notes if note['id']!= note_id]
    save_notes(notes)
    return redirect(url_for('home'))

# API wale routes - YE SABSE LAST MEIN
@app.route('/api/notes', methods=['GET'])
def get_notes_api():
    notes = load_notes()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note_api():
    notes = load_notes()
    new_id = notes[-1]['id'] + 1 if notes else 1
    data = request.get_json()
    note_text = data['text']
    notes.append({'id': new_id, 'text': note_text})
    save_notes(notes)
    return jsonify({'id': new_id, 'text': note_text}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)