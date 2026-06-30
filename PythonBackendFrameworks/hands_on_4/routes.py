from flask import Blueprint, jsonify, request

courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")

courses = [
    {
        "id": 1,
        "name": "Database Management Systems",
        "code": "CS101",
        "credits": 4
    }
]


def make_response(data, status_code=200):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


@courses_bp.route("/", methods=["GET"])
def get_courses():
    return make_response(courses)


@courses_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return make_response(course)


@courses_bp.route("/", methods=["POST"])
def create_course():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["name", "code", "credits"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_course = {
        "id": len(courses) + 1,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"]
    }

    courses.append(new_course)

    return make_response(new_course, 201)


@courses_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    course["name"] = data.get("name", course["name"])
    course["code"] = data.get("code", course["code"])
    course["credits"] = data.get("credits", course["credits"])

    return make_response(course)


@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    courses.remove(course)

    return jsonify({"message": "Course deleted successfully"}), 200