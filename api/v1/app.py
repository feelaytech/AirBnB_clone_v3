#!/usr/bin/python3
"""Starts Flask web application."""
from flask import Flask
import os
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)

host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = os.getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown(exc):
    """Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
