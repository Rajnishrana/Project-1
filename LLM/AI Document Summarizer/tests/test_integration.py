import pytest
from backend.app import app
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_flow(client):
    # Simulate a user query with context and question
    payload = {
        'context': 'Artificial Intelligence is ...',
        'question': 'Explain dropout in deep learning.'
    }
    response = client.post('/api/ask', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'answer' in data
    # Basic check answer is not empty
    assert len(data['answer']) > 0
