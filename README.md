# Language Learning Quiz Reminder 🇩🇪🇺🇦🤖

A Telegram-based AI assistant that helps users learn and retain German vocabulary through micro-quizzes. Designed for spaced repetition, this bot tracks user performance and motivates learning through friendly reminders and statistics.

---

## ✨ Features

- 🧠 **Micro Quiz Engine**: Sends random untranslated Ukrainian words and validates user translations.
- 👥 **Multi-user support**: Tracks individual learning progress for each user.
- 💾 **Data storage**: Supports Excel and SQLite backends.
- 💬 **Telegram Bot**: Simple interaction via Telegram messages.
- 🕒 **Motivation system**: Encourages users after inactivity with personal progress & leaderboard.
- 🧪 **Pytest test suite**: Includes unit tests for core modules and data loading logic.
- 🛠️ **Configuration-driven**: YAML-based settings and JSON secrets.

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/PKuts/language-learning-quiz-reminder.git
cd language-learning-quiz-reminder
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the bot

- Edit `config/config.yaml` — adjust data source and behavior settings
- Edit `config/secrets.json` — set your Telegram `BOT_TOKEN` and allowed `USER_IDS`

### 4. Run the bot

```bash
python main.py
```

---

## 📁 Project Structure

```
project/
├── bot/                  # Telegram interaction
├── config/               # YAML config and secrets
├── core/                 # Quiz logic and motivation
├── data/                 # Dictionary source, SQLite init
├── logs/                 # Logs by day
├── tests/                # Pytest tests
├── utils/                # Logger utility
├── main.py               # Main runner
├── requirements.txt
└── README.md
```

---

## ✅ Testing

```bash
pytest tests/
```

---

## 🧩 Dependencies

- `pandas`, `openpyxl`, `requests`, `pyyaml`, `pytest`
- Python 3.9+

---

## 📜 License

[MIT](LICENSE) © 2025 Pavlo Kuts