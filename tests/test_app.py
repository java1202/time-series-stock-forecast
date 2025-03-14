# tests/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Stock Time-Series Management & Forecasting" in response.data

# Additional tests for /fetch, /history, /forecast, and /visualize can be added here.
