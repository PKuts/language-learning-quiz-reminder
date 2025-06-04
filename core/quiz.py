import random
import time
from data.loader import save_dictionary
from telegram.handler import send_message
from utils.logger import log_message

def get_random_task(df, user_id, user_ids):
    """
    Select a new quiz task for a user.
    :param df: DataFrame with dictionary data.
    :param user_id: Telegram user ID.
    :param user_ids: List of all user IDs.
    :return: (row_index, word to translate) or (None, None) if nothing is left
    """
    user_column = f"User {user_ids.index(user_id) + 1}"
    filtered_df = df[df[user_column] == 0]

    if not filtered_df.empty:
        random_row = filtered_df.sample(n=1).iloc[0]
        return random_row.name, random_row["Ukrainian"]
    return None, None

def validate_response(df, row_index, user_id, user_ids, user_response, config, secrets):
    """
    Validate the user's translation response.
    :param df: DataFrame with dictionary data.
    :param row_index: Index of the row being validated.
    :param user_id: Telegram user ID.
    :param user_ids: List of all user IDs.
    :param user_response: The user's input text.
    :param config: General configuration dictionary.
    :param secrets: Secrets dictionary.
    """
    correct_translation = df.at[row_index, "German"]
    user_column = f"User {user_ids.index(user_id) + 1}"

    if user_response.strip().lower() == correct_translation.strip().lower():
        df.at[row_index, user_column] = 1
        emoji = random.choice(config["positive_emojis"])
        send_message(user_id, f"That's right! {emoji}")
        save_dictionary(df, config)
        log_message("Feedback", user_id, f"Correct response: {user_response}")
    else:
        example_value = df.at[row_index, "Example"]
        emoji = random.choice(config["negative_emojis"])
        send_message(
            user_id,
            f"That's not correct. {emoji} Correct is: {correct_translation}. Example: {example_value}",
            config["delay"]
        )
        log_message("Feedback", user_id, f"Incorrect response: {user_response}")

def all_words_learned(df, user_id, user_ids):
    """
    Check if the user has learned all the words.
    :param df: DataFrame with dictionary data.
    :param user_id: Telegram user ID.
    :param user_ids: List of all user IDs.
    :return: True if user has learned all words, False otherwise.
    """
    user_column = f"User {user_ids.index(user_id) + 1}"
    return df[user_column].sum() == len(df)

def send_congratulations(user_id):
    """
    Send a congratulations message to the user who learned all words.
    """
    send_message(user_id, "Congratulations. You already learned everything. You should add new words.")
    log_message("Achievement", user_id, "Learned all words.")