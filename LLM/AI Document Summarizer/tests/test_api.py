import pytest
from app import app  # adjust import if your Flask app instance is named or located differently

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_sample_document_endpoint(client):
    response = client.get('/api/sample_document')
    assert response.status_code == 200

    data = response.get_json()
    assert 'article' in data
    assert 'abstract' in data
    assert isinstance(data['article'], str)
    assert len(data['article']) > 0
    assert isinstance(data['abstract'], str)
    assert len(data['abstract']) > 0

def test_ask_endpoint_valid(client):
    payload = {
        'context': 'This is some context about AI.',
        'question': 'What is AI?'
    }
    response = client.post('/api/ask', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'answer' in data
    assert isinstance(data['answer'], str)

def test_ask_endpoint_missing_question(client):
    payload = {'context': 'Some context.'}
    response = client.post('/api/ask', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_ask_endpoint_empty_question(client):
    payload = {'context': 'Some context.', 'question': '   '}
    response = client.post('/api/ask', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_integration_sample_and_ask(client):
    # Get a sample document first
    sample_resp = client.get('/api/sample_document')
    assert sample_resp.status_code == 200
    sample_data = sample_resp.get_json()
    article = sample_data.get('article', '')
    assert article

    # Ask a question based on the sample document
    payload = {
        'context': article,
        'question': 'Please summarize the main idea.'
    }
    ask_resp = client.post('/api/ask', json=payload)
    assert ask_resp.status_code == 200
    ask_data = ask_resp.get_json()
    assert 'answer' in ask_data
    assert isinstance(ask_data['answer'], str)
