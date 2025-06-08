import os
import sqlite3
import sys

import pandas as pd

# Ensure the script can find the config module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config_loader import load_config

# Create directory if not exists
os.makedirs("data", exist_ok=True)

# Define SQLite DB path
config = load_config()
db_path = config["sqlite_path"]

# Define table structure
columns = ["German", "Ukrainian", "Example", "Date", "User 1", "User 2"]

print(f"Create sqlite db with some words in {db_path}")
entries = [
    # From IMG_20250606_001111793_HDR
    ("der Haushalt", "господарство", "Ich mache den Haushalt.", "2025-06-06", 0, 0),
    ("die Abteilung", "підрозділ", "Er arbeitet in der Abteilung.", "2025-06-06", 0, 0),
    ("nämlich", "тобто", "Ich komme später, nämlich um acht.", "2025-06-06", 0, 0),
    (
        "der Streit",
        "суперечка",
        "Es gab einen Streit zwischen uns.",
        "2025-06-06",
        0,
        0,
    ),
    ("von da an", "з того часу", "Von da an änderte sich alles.", "2025-06-06", 0, 0),
    (
        "Noch Ansicht + Gen",
        "на мою думку",
        "Noch meiner Ansicht nach ist das falsch.",
        "2025-06-06",
        0,
        0,
    ),
    ("sich rasieren", "голитися", "Er rasiert sich jeden Morgen.", "2025-06-06", 0, 0),
    (
        "sich schminken",
        "фарбуватися",
        "Sie schminkt sich vor dem Spiegel.",
        "2025-06-06",
        0,
        0,
    ),
    ("sich beeilen", "поспішати", "Beeil dich, der Bus kommt!", "2025-06-06", 0, 0),
    ("fangen", "ловити", "Er fängt den Ball.", "2025-06-06", 0, 0),
    ("raten", "радити", "Ich rate dir zur Ruhe.", "2025-06-06", 0, 0),
    (
        "das Lebewesen",
        "жива істота",
        "Der Mensch ist ein Lebewesen.",
        "2025-06-06",
        0,
        0,
    ),
    ("zeigen", "показувати", "Er zeigt mir das Foto.", "2025-06-06", 0, 0),
    ("heimlich", "таємно", "Sie trafen sich heimlich.", "2025-06-06", 0, 0),
    ("gehören", "належати", "Das Buch gehört mir.", "2025-06-06", 0, 0),
    ("die Kette", "ланцюжок", "Sie trägt eine goldene Kette.", "2025-06-06", 0, 0),
    ("arm", "бідний", "Er ist arm aber ehrlich.", "2025-06-06", 0, 0),
    ("die Anzeige", "оголошення", "Ich habe die Anzeige gelesen.", "2025-06-06", 0, 0),
    ("sterben", "померти", "Er starb jung.", "2025-06-06", 0, 0),
    (
        "hast du schon mal",
        "have you ever",
        "Hast du schon mal Pizza gegessen?",
        "2025-06-06",
        0,
        0,
    ),
    (
        "die Behinderung",
        "інвалідність",
        "Er lebt mit einer Behinderung.",
        "2025-06-06",
        0,
        0,
    ),
    (
        "unterschiedlich",
        "різний",
        "Die Meinungen sind unterschiedlich.",
        "2025-06-06",
        0,
        0,
    ),
    (
        "die Straßenbahn",
        "трамвай",
        "Ich fahre mit der Straßenbahn.",
        "2025-06-06",
        0,
        0,
    ),
    ("der Kuss", "поцілунок", "Sie gibt ihm einen Kuss.", "2025-06-06", 0, 0),
    ("sogar", "навіть", "Sogar das Kind weiß das.", "2025-06-06", 0, 0),
    ("übrigens", "до речі", "Übrigens, ich komme später.", "2025-06-06", 0, 0),
    ("der Dieb", "крадій", "Der Dieb wurde gefasst.", "2025-06-06", 0, 0),
    ("gelungen", "вдалий", "Das Experiment ist gelungen.", "2025-06-06", 0, 0),
    (
        "die Geschäftsreise",
        "відрядження",
        "Ich bin auf Geschäftsreise.",
        "2025-06-06",
        0,
        0,
    ),
    ("verpassen", "пропустити", "Ich habe den Zug verpasst.", "2025-06-06", 0, 0),
    ("bemalen", "малювати", "Die Kinder bemalen das Papier.", "2025-06-06", 0, 0),
    ("sein stolz auf", "пишатися", "Er ist stolz auf seinen Sohn.", "2025-06-06", 0, 0),
    ("kaum", "ледь", "Ich kann ihn kaum hören.", "2025-06-06", 0, 0),
    ("die Anzahl", "кількість", "Die Anzahl der Gäste steigt.", "2025-06-06", 0, 0),
    ("der Pass", "паспорт", "Ich habe meinen Pass vergessen.", "2025-06-06", 0, 0),
]

# Create DataFrame
df = pd.DataFrame(entries, columns=columns)

# Create and populate SQLite DB
conn = sqlite3.connect(db_path)
df.to_sql("dictionary", conn, if_exists="replace", index=False)
conn.close()
