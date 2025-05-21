import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ask_endpoint_success(client):
    response = client.post('/api/ask', json={
        'context': 'Dropout is a technique used in deep learning.',
        'question': 'What is dropout?'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'answer' in data
    assert isinstance(data['answer'], str)
    assert len(data['answer']) > 0

def test_ask_endpoint_missing_question(client):
    response = client.post('/api/ask', json={'context': 'some context', 'question': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing or empty question'

def test_ask_endpoint_invalid_json(client):
    response = client.post('/api/ask', data="notjson", content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
