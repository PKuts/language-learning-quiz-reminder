import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from project import send_message, create_dictionary, get_random_message

# Test for send_message
def test_send_message():
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        user_id = "123456"
        message = "Test message"

        send_message(user_id, message)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["data"] == {"chat_id": user_id, "text": message}

# Test for create_dictionary
def test_create_dictionary(tmp_path):
    file_path = tmp_path / "test_dictionary.xlsx"

    # Create a sample Excel file for testing
    data = {"Ukrainian": ["Привіт", "Дякую"], "German": ["Hallo", "Danke"], "User 1": [0, 0]}
    pd.DataFrame(data).to_excel(file_path, index=False)

    # Create dictionary using the temporary test file
    df = create_dictionary(file_path)

    assert not df.empty
    assert "Ukrainian" in df.columns
    assert "German" in df.columns

    # Test for missing file (the file does not exist, so the function should raise an error)
    with pytest.raises(SystemExit):
        create_dictionary("nonexistent_file.xlsx")


# Test for get_random_message
def test_get_random_message():
    data = {"Ukrainian": ["Привіт", "Дякую"], "German": ["Hallo", "Danke"], "User 1": [0, 1]}
    df = pd.DataFrame(data)

    row = get_random_message(df, "User 1")

    assert row is not None
    assert row["Ukrainian"] == "Привіт"

    # Test when no rows are available
    df["User 1"] = 1
    row = get_random_message(df, "User 1")
    assert row is None
