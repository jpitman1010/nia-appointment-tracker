import pytest
from server import app,  db, Staff 
from models.models import Role
import os

@pytest.fixture
def client():
    os.environ['FLASK_ENV'] = 'testing'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def login(client, roles):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # some dummy user id
        sess['roles'] = roles  # e.g. ['admin'], ['provider'], etc.
        sess['permissions'] = {
            "can_prescribe": "physician" in roles,
            "can_order_tests": True,
            # add other permissions you use or just keep empty dict
        }

def test_admin_access_allowed(client):
    login(client, ['admin'])
    response = client.get('/admin')
    assert response.status_code == 200

def test_admin_access_denied(client):
    login(client, ['clinician'])  # clinician does NOT have admin access
    response = client.get('/admin')
    assert response.status_code == 403

def test_staff_access_allowed(client):
    login(client, ['physician'])  # physician allowed on staff page
    response = client.get('/staff')
    assert response.status_code == 200

def test_staff_access_denied(client):
    login(client, ['guest'])  # guest not allowed
    response = client.get('/staff')
    assert response.status_code == 403
