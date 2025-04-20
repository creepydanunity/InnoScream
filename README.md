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
API_URL=<InnoScreamAPI_URL>
```

### 3.2 Create `app_fastapi/.env` file
```env
DB_FILENAME=innoscream.db
IMGFLIP_USERNAME=your_imgflip_username
IMGFLIP_PASSWORD=your_imgflip_password
```

## 🚀 Running the Project
### Via docker-compose:
```bash
TODO: fill
```

## 📡 Telegram Commands

| Command                     | Description                                      |
|-----------------------------|--------------------------------------------------|
| `/scream`                   | Submit a new anonymous scream                    |
| `/next`                     | Recieve next unseen scream                       |
| `/stress`                   | Get overall stress level of the current week     |
| `/my_stats`                 | Get stats for a user (anonymized by user ID)     |

## 📜 License

MIT License — feel free to use and modify.