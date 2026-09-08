import os

import pytest


os.environ["FLASK_DEBUG"] = "true"
os.environ["ADMIN_TOKEN"] = "test-admin-token"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "test-password"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app as flask_app


@pytest.fixture()
def app():
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()
