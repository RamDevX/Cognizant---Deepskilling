from flask import Flask, request, jsonify  # type: ignore[import]
import json
import urllib.request
import urllib.error

app = Flask(__name__)

COURSE_SERVICE = "http://127.0.0.1:5001"
STUDENT_SERVICE = "http://127.0.0.1:5002"


def _http_request(method, url, json_data=None):
    body = None
    headers = {"Content-Type": "application/json"}
    if json_data is not None:
        body = json.dumps(json_data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8")
            data = json.loads(payload) if payload else {}
            return _Response(data, resp.status)
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        try:
            data = json.loads(error_body) if error_body else {"message": error.reason}
        except json.JSONDecodeError:
            data = {"message": error_body or error.reason}
        return _Response(data, error.code)


class _Response:
    def __init__(self, payload, status_code):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload


class requests:
    @staticmethod
    def get(url):
        return _http_request("GET", url)

    @staticmethod
    def post(url, json=None):
        return _http_request("POST", url, json)


@app.route("/")
def home():
    return {
        "message": "API Gateway Running"
    }


@app.route("/api/courses", methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        response = requests.get(f"{COURSE_SERVICE}/api/courses")
    else:
        response = requests.post(
            f"{COURSE_SERVICE}/api/courses",
            json=request.json
        )

    return jsonify(response.json()), response.status_code


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def course_by_id(course_id):
    response = requests.get(
        f"{COURSE_SERVICE}/api/courses/{course_id}"
    )

    return jsonify(response.json()), response.status_code


@app.route("/api/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        response = requests.get(f"{STUDENT_SERVICE}/api/students")
    else:
        response = requests.post(
            f"{STUDENT_SERVICE}/api/students",
            json=request.json
        )

    return jsonify(response.json()), response.status_code


@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll(student_id):
    response = requests.post(
        f"{STUDENT_SERVICE}/api/students/{student_id}/enroll",
        json=request.json
    )

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(port=5000, debug=True)