from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///studentResult.db"
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    results = db.relationship("Result", backref = "student")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "results": [result.to_dict() for result in self.results]
        }


class Result(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String, nullable = False)
    score = db.Column(db.Float, nullable = False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "score": self.score,
            "student_id": self.student_id,
        }



with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Students results portal"})


@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student:
        return jsonify((student.to_dict()))
    else:
        return jsonify({"error": "Student not found"}), 404


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    new_student = Student(name=data["name"])

    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})


