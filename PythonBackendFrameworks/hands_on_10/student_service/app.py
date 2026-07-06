from flask import Flask, request, jsonify  # type: ignore[import]
from flask_sqlalchemy import SQLAlchemy  # type: ignore[import]
import requests  # type: ignore[import]

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "message": "Student Service Running"
    }


@app.route("/api/students", methods=["GET"])
def get_students():
    students = Student.query.all()

    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email
        }
        for s in students
    ])


@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.json

    student = Student(
        name=data["name"],
        email=data["email"]
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "id": student.id
    }), 201


@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    data = request.json

    course_id = data["course_id"]

    response = requests.get(
        f"http://127.0.0.1:5001/api/courses/{course_id}"
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Course not found"
        }), 404

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "error": "Student not found"
        }), 404

    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": "Student enrolled successfully"
    })


if __name__ == "__main__":
    app.run(port=5002, debug=True)