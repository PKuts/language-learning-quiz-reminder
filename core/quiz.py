import random
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
