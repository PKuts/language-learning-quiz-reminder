
# PROJECT TITLE: Language Learning Quiz Reminder 1.0

## Video Demo: https://youtu.be/QuRhq2yCz4I

## About the Program

This program was created by Pavlo Kuts as part of the CS50's Introduction to Programming with Python certification.
It is an open-source project designed to be a quiz game and a language-learning tool.
It uses the Telegram API to facilitate the interaction between users and the bot.
The program is written in Python 3.12.8 and is intended for educational purposes.
Please contact the author at kuts.pavel@gmail.com for inquiries or permissions.

## Purpose

The primary goal of this program is to help people learn new languages by providing a quiz game format.
The user can translate words from a customizable dictionary, with feedback provided based on the accuracy of their translations.

### Features:

- **Customizable Dictionary:** The dictionary can be easily replaced with an Excel file of similar structure.
- **User Management:** Players can be added by including their Telegram user IDs.
- **Game Flow:**
    - The program sends words/phrases to users for translation via Telegram API.
    - The program share statistics and motivation message (optional and configurable).
    - Tracks user progress and validates responses.
    - The first user to complete all words in the dictionary wins.

## Files and Structure

- **config.json**: Contains the Telegram bot token and user IDs for players.
{
  "BOT_TOKEN": "Your Telegram Token",
  "USER_IDS": ["Telegram user1_id", "Telegram user2_id"]
}
- **dictionary.xlsx**: An Excel file containing words for learning. The sample file supports learning Ukrainian-German for two players.
- **project.YYYY-MM-DD.log**: A log file for recording events at the INFO level. It can be activated using flags: ["--log", "-l", "log=true"].
- **project.py**: Main program code that runs the bot and handles interactions.
- **test_project.py**: Unit tests written in pytest to validate key functions of the program.
- **requirements.txt**: List of libraries required to run the program.
- **README.md**: Documentation for the project.

## Key Constants and Methods

### Global Constants:
- **BOT_TOKEN**: Telegram bot token.
- **USER_IDS**: List of Telegram user IDs for players.
- **INTERVAL_SECONDS**: Time interval (in seconds) between sending messages.
- **DELAY**: Delay before sending feedback to the player.
- **DICTIONARY_NAME**: Name of the dictionary file (e.g., "dictionary.xlsx").
- **URL**: URL for the Telegram API.
- **POSITIVE_EMOJIS**: List of emojis for correct answers.
- **NEGATIVE_EMOJIS**: List of emojis for incorrect answers.
- **MOTIVATION**: Boolean flag to enable or disable motivation messages.
- **TIME_TO_MOTIVATE**: Time threshold (in seconds) before sending motivation.

### Methods:
- **log_message(action, user_id, content)**: Logs actions taken by users (e.g., sending messages, giving feedback).
- **send_message(user_id, message, delay=0)**: Sends a message to the user with an optional delay.
- **create_dictionary(FILE_Name)**: Loads the dictionary from the specified Excel file.
- **get_random_message(df, user_column)**: Selects a random word/phrase for the user to translate.
- **get_user_response(offset=None)**: Fetches user responses from Telegram.
- **validate_translation(df, row_index, user_id, user_response)**: Validates the user's translation and updates progress in the dictionary.
- **motivation(user_id)**: Sends motivation statistics to the user.

## Prerequisites

1. **Set up a Telegram bot** and get your bot token.
2. **Install required libraries**: The libraries required for this project are listed in `requirements.txt`. You can install them using:
    ```
    pip install -r requirements.txt
    ```

3. **Players** need to have Telegram installed on their devices or use it online.

## Running the Program

### Step 1: Clone the repository
```
git clone
cd your-repository-directory
```

### Step 2: Install dependencies
```
pip install -r requirements.txt
```

### Step 3: Run the program
To start the Program, run the following command:
```
python project.py
```

The bot will begin sending messages to the users at regular intervals and track their progress.

## Running Unit Tests

To ensure that the program functions correctly, you can run the unit tests using pytest:
```
pytest test_project.py
```

The tests will verify that key methods are working as expected.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request or contact the author directly at kuts.pavel@gmail.com.

### Commercial Use
This program is for educational and personal use only. Commercial use is prohibited without prior permission from the author.

## Program Information

The code for this program was written in **January 2025**.
