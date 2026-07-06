from flask import Flask, request, jsonify  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "message": "Course Service Running"
    }


@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    return jsonify([
        {
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "credits": course.credits
        }
        for course in courses
    ])


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits
    })


@app.route("/api/courses", methods=["POST"])
def create_course():
    data = request.json

    course = Course(
        name=data["name"],
        code=data["code"],
        credits=data["credits"]
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "id": course.id
    }), 201


if __name__ == "__main__":
    app.run(port=5001, debug=True)