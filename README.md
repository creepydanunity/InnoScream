# InnoScream – Anonymous Student Scream Platform

A Telegram-integrated platform where students can anonymously share their academic frustrations, support each other with reactions, and get memes + weekly analytics — all via an AI-powered backend built with FastAPI.

---

## ⚙️ Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async)
- **Database:** SQLite (using `aiosqlite`)
- **Bot Framework:** aiogram (Telegram)
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

### 3. Create `.env` file

```env
DB_FILENAME=innoscream.db
IMGFLIP_USERNAME=your_imgflip_username
IMGFLIP_PASSWORD=your_imgflip_password
```

## 🚀 Running the Project
### Start the FastAPI server:
```bash
poetry run uvicorn app_fastapi.main:app --reload
```
Visit:
- 📚 API docs (`Swagger UI`): http://localhost:8000/docs
- 📄 ReDoc: http://localhost:8000/redoc

## 📡 API Routes

Method | Route | Description
POST | `/scream` | Submit a new anonymous scream
POST | `/react` | React to a scream (💀, 🔥, 🥲)
GET | `/top` | Get top N screams of the day + memes
DELETE | `/delete/{scream_id}` | Admin delete a scream
GET | `/stats/{user_id}` | Get user's stats and weekly scream graph
GET | `/stats/weekly` | Get overall community scream graph

## 📜 License

MIT License — feel free to use and modify.