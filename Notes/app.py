from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy #For database
from datetime import datetime

#Creating an app
app = Flask(__name__)

#Connecting to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///personalNotes.db"
db = SQLAlchemy(app)

#Creating the database table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.String, nullable=False)
    updatedAt = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

with app.app_context():
    db.create_all() #Creates the database


@app.route("/")
def home():
    return jsonify({"message": "Welcome to personal notes"})


@app.route("/notes", methods=["GET"])
def get_notes():
    notes = User.query.all() # Gets all info and stores it in notes
    return jsonify([note.to_dict() for note in notes]) #Loops through each note


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = User.query.get(note_id)
    if note:
        return jsonify(note.to_dict())
    else:
        return jsonify({"error": "Notes not found"}), 404


@app.route("/notes", methods=["POST"]) # A method used to send info to the server
def add_note():
    data = request.get_json()
    new_notes = User(
        title=data["title"],
        content=data["content"],
        createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updatedAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(new_notes)
    db.session.commit()
    return jsonify(new_notes.to_dict()), 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
def find_note(note_id): # A method that is used to replace a note by its id
    note = User.query.get(note_id) #Find notes by ID
    if not note: #Check if it exists
        return jsonify({"error": "Note not found"}), 404
    else:
        data = request.get_json() #Read the new data from the request
        # Updates all fields
        note.title = data["title"]
        note.content = data["content"]
        note.updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return jsonify(note.to_dict())


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = User.query.get(note_id)
    if not note: #Check if it exists
        return jsonify({"error": "Note not found"}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully"})


if __name__ == "__main__": #Refresh
    app.run(debug=True)