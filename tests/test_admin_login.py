import pytest
from unittest.mock import MagicMock, patch
from model.admin import Admin

@pytest.fixture
def mock_database():
    with patch("model.admin.Database") as mock_db:
        yield mock_db

def test_authenticate_success(mock_database):
    """
    Test successful admin authentication.
    """

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_database.return_value.connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "email": "admin@bazar.com",
        "password": "admin123",
    }

    admin = Admin()

    result = admin.authenticate("admin@bazar.com", "admin123")

    assert result is True
    mock_cursor.execute.assert_called_once()


def test_authenticate_failure_invalid_credentials(mock_database):
    """
    Test authentication failure with invalid credentials.
    """

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_database.return_value.connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    admin = Admin()

    result = admin.authenticate("sadia@email.com", "sadia")

    assert result is False


def test_authenticate_database_connection_failure(mock_database):
    """
    Test authentication when database connection fails.
    """

    mock_database.return_value.connect.return_value = None

    admin = Admin()
    result = admin.authenticate("admin@bazar.com", "admin123")

    assert result is False
