from flask import Flask
from flask_migrate import Migrate  # type: ignore[import]

from config import Config
from models import db
from routes import courses_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(courses_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)