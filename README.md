# Telegram Shop Bot

A Telegram bot for selling products and services for **Telegram Stars (⭐️)**. Built with [aiogram 3](https://docs.aiogram.dev/en/v3.30.0/) and [SQLite](https://www.sqlite.org/docs.html). The catalog and orders are managed right from the chat through an admin panel, and the interface is bilingual (Russian / English).

## Features

**For customers**
- Language choice on first launch (RU / EN), remembered afterwards
- Catalog with two sections, **products** and **services**, with pagination
- Item card with name, description and price in ⭐️
- Payment via Telegram Stars (invoice link)
- Automatic delivery of the order content right after payment
- Purchase history and a profile page (language, registration date)

**For admins**
- Admin panel available only to users with admin rights
- List of all sales with details (date, price, refund status)
- **Stars refund** in one tap
- Catalog editor: create items, edit name, description, price and delivery content separately for each language, with preview
- Visibility settings: hide an item manually, or automatically after a sale (handy for one-of-a-kind items)

## Tech stack

- [Python](https://www.python.org) 3.10+
- [aiogram](https://docs.aiogram.dev/en/v3.30.0/) 3.30 for the Telegram Bot API
- [aiosqlite](https://aiosqlite.omnilib.dev/en/stable/index.html) for async SQLite access
- [python-dotenv](https://pypi.org/project/python-dotenv/) for configuration via `.env`

## Quick start

### 1. Get a bot token

Create a bot with [@BotFather](https://t.me/BotFather) and save the token. Payments in Stars (currency `XTR`) don't require a payment provider.

### 2. Clone the repository

```bash
git clone https://github.com/lornamixe/Telegram-Shop-Bot
cd Telegram-Shop-Bot
```

### 3. Run the setup

```bash
python setup.py
```

The script performs four steps:

1. creates a virtual environment in `venv/`;
2. installs dependencies from `requirements.txt`;
3. asks for `BOT_TOKEN` and the admins' Telegram IDs and writes them to `.env`;
4. creates the database and assigns admins (`init_db.py`).

You can find your Telegram ID with a bot such as [@userinfobot](https://t.me/userinfobot).

### 4. Start the bot

```bash
python run.py
```

## Configuration

Settings live in the `.env` file in the project root:

| Variable    | Description                                                       |
|-------------|-------------------------------------------------------------------|
| `BOT_TOKEN` | Bot token from @BotFather                                         |
| `ADMIN_IDS` | Comma-separated Telegram IDs of admins, e.g. `123,456`            |

To add an admin later, append their ID to `ADMIN_IDS` and run `python init_db.py` again.

> ⚠️ `.env` and `*.db` files are listed in `.gitignore`. Never publish your bot token.

## Manual installation

If you'd rather not use `setup.py`:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "BOT_TOKEN=your_token" > .env
echo "ADMIN_IDS=your_telegram_id" >> .env
python init_db.py
python main.py
```

## Project structure

```
project/
├── main.py              # entry point: bot, dispatcher, middlewares
├── run.py               # runs main.py inside the venv
├── setup.py             # setup: venv, dependencies, .env, database
├── init_db.py           # creates tables and assigns admins
├── routers.py           # list of all routers
├── config.py            # project and database paths
└── bot/
    ├── handlers/        # start, catalog, item cards, payment, refunds, language, profile
    │   └── admin/       # admin panel and catalog editor
    ├── callbacks/       # CallbackData factories for inline buttons
    ├── keyboards/       # keyboard builders
    ├── middlewares/     # language detection and admin check
    ├── database/        # SQLite access (users, items, sales)
    ├── locales/         # interface translations (ru / en)
    └── states/          # FSM states
```

## Database

The SQLite file is created at `bot/database/bot.db`. Tables:

- **Users**: user ID, language, registration date, admin flag
- **Product** and **Service**: catalog items (price, name / description / delivery content in two languages, visibility flags)
- **Sales**: sales (Telegram payment charge ID, amount, item, user, date, refund status)

## How it works

1. The user picks an item and the bot creates a Stars invoice.
2. Before payment (`pre_checkout_query`) the bot checks that the item isn't hidden and the price hasn't changed.
3. After payment the sale is saved to the database, the item is hidden if configured to be, and the user receives the order content.
4. An admin can refund the Stars from the sales section, and the order status is updated in the database.

## Limitations

- Item name is limited to 14 characters (stricter than Telegram's 32, so it fits on catalog buttons) and description to 255 (same as Telegram's limit).
- FSM state is kept in memory and resets when the bot restarts (language and admin rights are reloaded from the database).
- The bot uses long polling.

## What I learned

This project was a way to practice building a complete, working bot rather than isolated examples. Along the way I got hands-on with:

- **Middleware**: what it is and how it sits between a request and a response to process data.
- **State**: the core idea of state
- **Git**: started using Git for version control and tracking changes in my project.

