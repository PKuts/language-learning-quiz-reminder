import random
import time
from data.loader import save_dictionary
from bot.handler import send_message
from utils.logger import log_message

def get_random_task(df, user_id, user_ids):
    user_column = f"User {user_ids.index(user_id) + 1}"
    filtered_df = df[df[user_column] == 0]
    if not filtered_df.empty:
        random_row = filtered_df.sample(n=1).iloc[0]
        return random_row.name, random_row["Ukrainian"]
    return None, None

def validate_response(df, row_index, user_id, user_ids, user_response, config, secrets):
    correct_translation = df.at[row_index, "German"]
    user_column = f"User {user_ids.index(user_id) + 1}"

    if user_response.strip().lower() == correct_translation.strip().lower():
        df.at[row_index, user_column] = 1
        emoji = random.choice(config["positive_emojis"])
        send_message(user_id, f"That's right! {emoji}", bot_token=secrets["BOT_TOKEN"])
        save_dictionary(df, config)
        log_message("Feedback", user_id, f"Correct response: {user_response}")
    else:
        example = df.at[row_index, "Example"]
        emoji = random.choice(config["negative_emojis"])
        send_message(
            user_id,
            f"That's not correct. {emoji} Correct is: {correct_translation}. Example: {example}",
            delay=config["delay"],
            bot_token=secrets["BOT_TOKEN"]
        )
        log_message("Feedback", user_id, f"Incorrect response: {user_response}")

def all_words_learned(df, user_id, user_ids):
    user_column = f"User {user_ids.index(user_id) + 1}"
    return df[user_column].sum() == len(df)

def send_congratulations(user_id):
    send_message(user_id, "🎉 Congratulations! You’ve learned everything. Add new words to continue!")
    log_message("Achievement", user_id, "Learned all words.")

def send_motivation(df, user_id, user_ids, config, secrets):
    """
    Send a motivational message to the user, including stats and competition.
    """
    user_column = f"User {user_ids.index(user_id) + 1}"
    total_words = len(df)
    learned_words = df[user_column].sum()
    percent = round(learned_words / total_words * 100)

    # Lets find Leader
    leaderboard = {
        uid: df[f"User {user_ids.index(uid) + 1}"].sum() for uid in user_ids
    }
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    message = f"You’ve learned {learned_words} out of {total_words} words ({percent}%). Keep going!"

    # If there're more than one player
    if len(sorted_leaderboard) > 1 and sorted_leaderboard[0][0] != user_id:
        leader_id, leader_score = sorted_leaderboard[0]
        message += f"\n Your friend is leading with {leader_score} words. Try to catch up!"

    send_message(user_id, message, bot_token=secrets["BOT_TOKEN"])
    log_message("Motivation", user_id, message)