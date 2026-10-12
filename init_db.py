import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_env(path):
    result = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                result[key.strip()] = value.strip()
    return result


DB_PATH = Path(__file__).resolve().parent / "bot" / "database" / "bot.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

ITEM_COLUMNS = """
    Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    Cost INTEGER NOT NULL DEFAULT 100,
    Name_ru TEXT NOT NULL DEFAULT 'Название',
    Description_ru TEXT NOT NULL DEFAULT 'Описание',
    Name_en TEXT NOT NULL DEFAULT 'Title',
    Description_en TEXT NOT NULL DEFAULT 'Description',
    Delivery_content_ru TEXT DEFAULT 'Текст',
    Delivery_content_en TEXT DEFAULT 'Text',
    Hide_after_sale INTEGER NOT NULL DEFAULT 0,
    Is_hidden INTEGER DEFAULT 0
"""

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS Users (
    User_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Language TEXT DEFAULT 'en',
    Registration_date TEXT NOT NULL DEFAULT (CURRENT_DATE),
    Is_admin INTEGER DEFAULT 0 NOT NULL
);
CREATE TABLE IF NOT EXISTS Sales (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Charge_id TEXT NOT NULL UNIQUE,
    Amount INTEGER NOT NULL,
    Item_id INTEGER NOT NULL,
    Item_type TEXT NOT NULL,
    User_id INTEGER NOT NULL,
    Date TEXT DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    Status INTEGER DEFAULT 0 NOT NULL
);
CREATE TABLE IF NOT EXISTS Service ({ITEM_COLUMNS});
CREATE TABLE IF NOT EXISTS Product ({ITEM_COLUMNS});
"""

admin_ids = [int(x) for x in read_env(ROOT / ".env").get("ADMIN_IDS", "").replace(" ", "").split(",") if x.isdigit()]

with sqlite3.connect(DB_PATH) as conn:
    conn.executescript(SCHEMA)
    for uid in admin_ids:
        conn.execute(
            "INSERT INTO Users (User_id, Language, Is_admin) VALUES (?, NULL, 1) "
            "ON CONFLICT(User_id) DO UPDATE SET Is_admin = 1",
            (uid,),
        )

print(f"DB created: {DB_PATH}")
if admin_ids:
    print(f"Admins: {', '.join(map(str, admin_ids))}")
