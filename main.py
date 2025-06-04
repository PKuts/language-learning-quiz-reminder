from config.config_loader import load_config, load_secrets
from data.loader import load_dictionary
from utils.logger import setup_logging, log_message

# Load configuration files
config = load_config()
secrets = load_secrets()

# Load sensitive data
BOT_TOKEN = secrets["BOT_TOKEN"]
USER_IDS = secrets["USER_IDS"]

# Load general configuration
INTERVAL_SECONDS = config["interval_seconds"]
DELAY = config["delay"]
MOTIVATION = config["motivation_enabled"]
TIME_TO_MOTIVATE = config["motivation_timeout"]
DICTIONARY_NAME = config["excel_path"]

# Feedback emoji
POSITIVE_EMOJIS = config["positive_emojis"]
NEGATIVE_EMOJIS = config["negative_emojis"]

# Setup logging
logging_config = config.get("logging", {})
setup_logging(
    enable=logging_config.get("enabled", False),
    log_path=logging_config.get("file", "logs/project.log")
)


print (POSITIVE_EMOJIS)

df = load_dictionary(config)
print(df.head())