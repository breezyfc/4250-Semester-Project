import pytest
# smoke tests for login functionality and navigation

# flask app is imported only once
@pytest.fixture(scope="module")
def flask_app():
    from flask_application import server

    server.app.config["TESTING"] = True
    return server.app


# client is created only once
@pytest.fixture
def flask_client(flask_app):
    return flask_app.test_client()

# testing that the registration page should load for anonymous users
def test_register_get_returns_200(flask_client):
    response = flask_client.get("/register")
    assert response.status_code == 200

# testing that the login page should load for anonymous users
def test_login_get_returns_200(flask_client):
    response = flask_client.get("/login")
    assert response.status_code == 200

# testing that the dashboard should require authentication and redirect unauthenticated users
def test_home_requires_login_redirect(flask_client):
    response = flask_client.get("/", follow_redirects=False)
    assert response.status_code in (302, 401)