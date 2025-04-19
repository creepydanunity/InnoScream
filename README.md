# InnoScream – Anonymous Student Scream Platform (API)

An API developed for Telegram-integrated platform where students can anonymously share their academic frustrations, support each other with reactions, and get memes + weekly analytics.

---

## ⚙️ Tech Stack

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
git checkout api
```

### 2. Set up virtual environment (recommended via Poetry)

```bash
poetry install
```

### 3. Create `app_fastapi/.env` file

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

| Method   | Endpoint                    | Description                                      |
|----------|-----------------------------|--------------------------------------------------|
| `POST`   | `/scream`                   | Submit a new anonymous scream                   |
| `POST`   | `/react`                    | React to a scream                               |
| `GET`    | `/top?n=3`                  | Get top N screams of the day + meme links       |
| `GET`    | `/stats/{user_id}`          | Get stats for a user (anonymized by user ID)    |
| `GET`    | `/stats/weekly/{user_id}`   | Weekly scream graph for a user                  |
| `GET`    | `/stats/weekly`             | Weekly scream graph for all users               |
| `DELETE` | `/delete/{scream_id}`       | Delete a scream (admin only)                    |

## 📜 License

MIT License — feel free to use and modify.