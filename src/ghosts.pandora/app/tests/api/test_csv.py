from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

@pytest.mark.parametrize("method", ["get", "post"])
def test_return_csv_with_ollama_enabled():
    response = getattr(client, method)("/csv/test")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'

@pytest.mark.parametrize("method", ["get", "post"])
def test_return_csv_with_ollama_disabled():
    response = getattr(client, method)("/csv/test")
    assert response.status_code == 200
    assert response.headers["Content-Disposition"] == 'inline; filename="test.csv"'

@pytest.mark.parametrize("method", ["get", "post"])
def test_return_csv_with_random_name():
    response = getattr(client, method)("/csv/")
    assert response.status_code == 200
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"].endswith('.csv"')
