import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest

from core.quiz import all_words_learned, get_random_task


@pytest.fixture
def sample_df():
    data = {
        "German": ["der Hund", "die Katze"],
        "Ukrainian": ["собака", "кіт"],
        "Example": ["Der Hund bellt.", "Die Katze schläft."],
        "Date": ["2025-06-01", "2025-06-02"],
        "User 1": [0, 1],
        "User 2": [1, 1],
    }
    return pd.DataFrame(data)


def test_get_random_task_returns_unlearned(sample_df):
    row_index, word = get_random_task(
        sample_df, user_id="user1", user_ids=["user1", "user2"]
    )
    assert word in sample_df["Ukrainian"].values


def test_all_words_learned_false(sample_df):
    assert (
        all_words_learned(sample_df, user_id="user1", user_ids=["user1", "user2"])
        == False
    )


def test_all_words_learned_true():
    df = pd.DataFrame(
        {
            "German": ["eins"],
            "Ukrainian": ["один"],
            "Example": ["Das ist eins."],
            "Date": ["2025-06-01"],
            "User 1": [1],
            "User 2": [1],
        }
    )
    assert all_words_learned(df, user_id="user1", user_ids=["user1", "user2"]) == True
