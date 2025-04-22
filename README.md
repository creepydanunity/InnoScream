# InnoScream – Anonymous Student Scream Platform

A Telegram-integrated platform where students can anonymously share their academic frustrations, support each other with reactions, and get memes + weekly analytics.

---

## ⚙️ Tech Stack

- **Bot:** Python 3.11, aiogram (Telegram), httpx, asyncio
- **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async)
- **Database:** SQLite (using `aiosqlite`)
- **External APIs:**  
  - 📊 [QuickChart.io](https://quickchart.io/) – Weekly analytics graphs  
  - 🖼️ [ImgFlip Meme API](https://imgflip.com/api) – Meme generation

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/creepydanunity/innoscream.git
cd innoscream
```

### 2. Set up virtual environment (recommended via Poetry)

```bash
poetry install
```

### 3.1 Create `app_bot/.env` file
```env
BOT_TOKEN=<TelegramAPI_Token>
API_URL=<InnoScreamAPI_URL> (default: http://api:8000)
```

### 3.2 Create `app_fastapi/.env` file
```env
DB_FILENAME=your_sqlite_db_name (default: innoscream.db)
IMGFLIP_API_USERNAME=your_imgflip_username
IMGFLIP_API_PASSWORD=your_imgflip_password
DEFAULT_ADMIN_ID=your_telegram_id
```

## 🚀 Running the Project
### Via docker-compose:
- In `InnoScream/`
```bash
docker-compose up --build
```

## 📡 Telegram Commands

| Command                     | Description                                       |
|-----------------------------|---------------------------------------------------|
| `/scream`                   | Submit a new anonymous scream                     |
| `/feed`                     | Recieve next unseen scream                        |
| `/stress`                   | Get overall stress level of the current week      |
| `/my_stats`                 | Get stats for a user (anonymized by user ID)      |
| `/delete`                   | Open scream moderation panel                      |
| `/my_id`                    | Get your telegram_id (for testing purposes)       |
| `/create_admin`             | Add user as admin (telegram_id as param required) |

## 📜 License

MIT License — feel free to use and modify.