from unittest.mock import patch

import pytest

from api import routes
from api.routes import post_login


@patch("requests.post")
def test_login(mock_post):
    # Arrange
    mock_post.return_value.json.return_value = {
        "access_token": "token",
    }
    email = "lucas@"
    senha = "123"

    # Act
    response = post_login(email, senha)

    # Assert
    assert response["access_token"] == "token"
