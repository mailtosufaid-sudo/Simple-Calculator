import os

from flask import Flask, send_from_directory


def create_app():
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
    app = Flask(__name__, static_folder=static_dir, static_url_path="/static")

    from .routes import bp
    app.register_blueprint(bp)

    @app.route("/")
    def index():
        return send_from_directory(static_dir, "index.html")

    return app
