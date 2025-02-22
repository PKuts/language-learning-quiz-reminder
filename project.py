import time
from datetime import datetime
import requests
import os
import pandas as pd
import random
import logging
import sys
import json


# Load Telegram bot token and List of Telegram users from config.json
with open("config.json") as file:
    config = json.load(file)
BOT_TOKEN = config["BOT_TOKEN"]
USER_IDS  = config["USER_IDS"]

# Frequency with which messages will be sent
INTERVAL_SECONDS = 5

# Delay for verification feedback
DELAY = 0

# File dictionary
DICTIONARY_NAME = "dictionary.xlsx"

# URL to run Telegram API
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Emoji lists for feedback.Emojis for correct answers
POSITIVE_EMOJIS = ["😊", "🎉", "👍", "🌟", "😁"]

# Emoji lists for feedback.Emojis for incorrect answers
NEGATIVE_EMOJIS = ["😞", "🙃", "😅", "😔", "👎"]

# Boolean variable to enable user motivation by sharing statistics
MOTIVATION = True

# The waiting time for a user's response in seconds, after which motivation is triggered
TIME_TO_MOTIVATE = 600

# Global variable for controlling the timely sending of motivational messages and providing statistics.
last_response_time = {user_id: time.time() for user_id in USER_IDS}

# Logger setup
ENABLE_LOGGING = any(arg in ["--log", "-l", "log=true"] for arg in sys.argv)
if ENABLE_LOGGING:
    log_filename = f"project.{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Program started.")

def log_message(action, user_id, content):
    """
    Log messages for user actions.
    :param action: Action type (e.g., "Sent", "Feedback", "Achievement").
    :param user_id: Telegram user ID.
    :param content: Content of the action.
    """
    if ENABLE_LOGGING:
        logging.info(f"{action} | User: {user_id} | Content: {content}")

def send_message(user_id, message, delay = 0):
    """
    Send message to user.
    :param user_id: Telegram user ID.
    :param message: Message text.
    :param delay: Delay before sending the message, in seconds.
    """
    if delay > 0:
       time.sleep(delay)  # Wait before sending

    data = {
        "chat_id": user_id,
        "text": message
    }

    response = requests.post(f"{URL}/sendMessage", data=data)
    if response.status_code == 200:
        last_response_time[user_id] = time.time()
        print(f"{message} sent to user {user_id}")
        log_message("Sent", user_id, message)
    else:
        print(f"User error {user_id}: {response.status_code}, {response.text}")

def create_dictionary (FILE_Name):
    """
    Verify if excel file exists and load it to pandas DataFrame.
    :param FILE_Name: Path to the file(f.e. 'dictionary.xlsx').
    :return: DataFrame with data or message that file not exists
    """
    # Verify if excel file exists
    if not os.path.exists(FILE_Name):
        print(f"File {FILE_Name} not found. The program will terminate")
        exit()

    # Load file to the DataFrame
    try:
        df = pd.read_excel(FILE_Name)  # Read Excel
        df.columns = df.columns.str.strip()  # Removes spaces
        print(f"File {FILE_Name} successfully uploaded.")
        return df
    except Exception as e:
        print(f"Some error occurred while uploading the file: {e}")
        exit()

def get_random_message (df, user_column):
    """
    Select text that users suppose to translate randomly
    :param df: DataFrame with Dictionary data.
    :param user_column: Flag that shows if this text has been correctly translated by user.
    :return: Text that will be send for translation or None if no available rows exist
    """
    filtered_df = df[df[user_column] == 0]  # Filter to use only rows with user flag == 0
    if not filtered_df.empty:
        random_row = filtered_df.sample(n = 1).iloc[0]  # Random row
        #return random_row["Ukrainian"]  # Ukrainian text in Random row
        return random_row # Return rabdomly selected row
    return None

def get_user_response(offset = None):
    """
    Fetch user responses (messages) from Telegram API.
    :param offset: Offset to get new updates.
    :return: List of user messages received.
    """
    response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 10})
    if response.status_code == 200:
        updates = response.json().get("result", [])
        print(f"Received updates: {updates}")
        return updates
    else:
        print(f"Error fetching user responses: {response.status_code}, {response.text}")
        return []

def validate_translation(df, row_index, user_id, user_response):
    """
    Validate user's translation.
    :param df: DataFrame with the dictionary data.
    :param row_index: Index of the row being validated.
    :param user_id: Telegram user ID.
    :param user_response: User's translation response.
    """
    last_response_time[user_id] = time.time()
    correct_translation = df.at[row_index, "German"]


    if user_response.strip().lower() == correct_translation.strip().lower():
        df.at[row_index, f"User {USER_IDS.index(user_id) + 1}"] = 1
        emoji = random.choice(POSITIVE_EMOJIS)
        send_message(user_id, f"That's right! {emoji}")

        df.to_excel(DICTIONARY_NAME, index=False)  # Save changes to Excel after the correct answer, use False to avoid adding index column
        print(f"Changes saved to {DICTIONARY_NAME}.")
        log_message("Feedback", user_id, f"Correct response: {user_response}")

    else:
        example_value = df.at[row_index, "Example"]
        emoji = random.choice(NEGATIVE_EMOJIS)
        send_message(user_id, f"That's not correct. {emoji} Correct is: {correct_translation}. Example: {example_value}", DELAY)
        log_message("Feedback", user_id, f"Incorrect response: {user_response}")

def motivation (user_id):
    """
    Motivation function to share current statistics with users
    :param user_id: Telegram user ID.
    """
    df = create_dictionary(DICTIONARY_NAME)
    total_words = len(df) # Get total number of rows in dictionary

    # Get current user statistics
    user_column = f"User {USER_IDS.index(user_id) + 1}"
    user_correct = df[user_column].sum()

    # Get statistics for other users
    opponent_stats = []
    for i, other_user_id in enumerate(USER_IDS):
        if other_user_id != user_id:
            opponent_column = f"User {i + 1}"
            opponent_correct = df[opponent_column].sum()
            opponent_stats.append(f"Your opponent user {i + 1} answered {opponent_correct} questions from {total_words}")

    # Create the motivation message
    message =  f"Hey, you haven't responded in a while ( {TIME_TO_MOTIVATE} seconds). It's too long. Do you even want to win?! Look at the statistics and play better!:\n"
    message += f"You answered correctly {user_correct} questions from {total_words}.\n"
    message += "\n".join(opponent_stats)

    # Send the message to the user
    send_message(user_id, message)

def main():

        print(f"The program is running. Messages will be sent every {INTERVAL_SECONDS} seconds.")

        df = create_dictionary (DICTIONARY_NAME)
        print(df.head())  # Verify table structure, print the first 5 rows of dictionary table

        offset = None
        user_current_tasks = {user_id: None for user_id in USER_IDS}
        last_task_time = {user_id: 0 for user_id in USER_IDS}
        current_time = time.time()

        try:
            while True:
                current_time = time.time()

                # Check if any user has learned all words
                for i, user_id in enumerate(USER_IDS):
                    user_column = f"User {i+1}"

                # Check if all values in the user's column are 1 (meaning all words are learned)
                    if df[user_column].sum() == len(df):
                        send_message(user_id, "Congratulations. You already learn everything.You should add new words.")
                        print(f"User {i+1} has learned all words.")
                        log_message("Achievement", user_id, "Learned all words.")
                        print(f"We found the Hero! {user_id} is the WINNER! The program will terminate.")
                        exit()

                # Send new tasks at INTERVAL_SECONDS
                for user_id in USER_IDS:
                    if user_current_tasks[user_id] is None and current_time - last_task_time[user_id] >= INTERVAL_SECONDS:
                        random_row = get_random_message(df, f"User {USER_IDS.index(user_id) + 1}")
                        if random_row is not None:
                            user_current_tasks[user_id] = random_row.name  # Store the index of the random row
                            send_message(user_id, random_row["Ukrainian"])
                            last_task_time[user_id] = current_time  # Timestamp, last task time update

                    # Check if user has not responded and we want to motive user by statistick sharing
                    if user_current_tasks[user_id] is not None and current_time - last_response_time[user_id] >= TIME_TO_MOTIVATE and MOTIVATION:
                        motivation(user_id)
                        last_response_time[user_id] = current_time

                # Fetch user responses
                updates = get_user_response(offset)
                for update in updates:
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    user_id = str(message.get("from", {}).get("id", ""))
                    text = message.get("text", "")

                    if user_id in USER_IDS and user_current_tasks[user_id] is not None:
                        validate_translation(df, user_current_tasks[user_id], user_id, text)
                        user_current_tasks[user_id] = None

                time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
               print("Program terminated by user.")
               logging.info("Program terminated by user.")


if __name__ == '__main__':
    main()
