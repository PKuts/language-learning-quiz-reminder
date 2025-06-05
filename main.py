import time
from config.config_loader import load_config, load_secrets
from data.loader import load_dictionary
from bot.handler import send_message, fetch_updates
from utils.logger import setup_logging, log_message
from core.quiz import get_random_task, validate_response, all_words_learned, send_congratulations, send_motivation

# Load configuration
config = load_config()
secrets = load_secrets()

# Logging
logging_config = config.get("logging", {})  
setup_logging(
    enable=logging_config.get("enabled", False),
    log_path=logging_config.get("file", "logs/quiz.log"),
    level=logging_config.get("level", "INFO")
)

BOT_TOKEN = secrets["BOT_TOKEN"]
USER_IDS = secrets["USER_IDS"]
INTERVAL_SECONDS = config["interval_seconds"]
TIME_TO_MOTIVATE = config["motivation_timeout"]
MOTIVATION = config["motivation_enabled"]

# Load dictionary
df = load_dictionary(config)
offset = None
user_tasks = {user_id: None for user_id in USER_IDS}
last_task_time = {user_id: 0 for user_id in USER_IDS}
last_response_time = {user_id: time.time() for user_id in USER_IDS}

print("Bot is running...")

try:
    while True:
        now = time.time()

        for user_id in USER_IDS:
            if all_words_learned(df, user_id, USER_IDS):
                send_congratulations(user_id)
                print(f"{user_id} learned all words. Let's congratulate the winner!!! Exiting...")
                exit()

            if user_tasks[user_id] is None and now - last_task_time[user_id] >= INTERVAL_SECONDS:
                row_index, word = get_random_task(df, user_id, USER_IDS)
                if word:
                    user_tasks[user_id] = row_index
                    send_message(user_id, word, bot_token=BOT_TOKEN)
                    last_task_time[user_id] = now

            if user_tasks[user_id] is not None and now - last_response_time[user_id] > TIME_TO_MOTIVATE and MOTIVATION:
                send_motivation(df, user_id, USER_IDS, config, secrets)
                last_response_time[user_id] = now

        updates = fetch_updates(offset=offset, bot_token=BOT_TOKEN)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message", {})
            user_id = str(message.get("from", {}).get("id", ""))
            text = message.get("text", "")

            if user_id in USER_IDS and user_tasks[user_id] is not None:
                validate_response(df, user_tasks[user_id], user_id, USER_IDS, text, config, secrets)
                user_tasks[user_id] = None
                last_response_time[user_id] = time.time()

        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Bot stopped by user.")