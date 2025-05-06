# InnoScream – Anonymous student scream platform
## 🎯 Project goal

> Build a Telegram-based anonymous stress relief platform for students, where users can post frustrations, react with emojis, view community stress stats, and see top daily screams as memes.

---

### ⚙️ Tech stack

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
USER_ID_SALT=your_user_id_salt
```

### Running the project:
- In `InnoScream/`
```bash
docker-compose up --build
```
---
## 📜 License

MIT License — feel free to use and modify.

---
# Functionality
## 📦 System architecture

The project is composed of two isolated services:

- `app_fastapi` — REST API backend handling data storage, analytics, and moderation.
- `app_bot` — Telegram bot built with `aiogram`, serving as the frontend interface for users.

Each service runs in its own Docker container for modularity and deployment flexibility.

---
## ✅ Implemented features overview

| Feature                      | Description                                                                 | Status |
|-----------------------------|-----------------------------------------------------------------------------|--------|
| **Anonymous screams**       | `/scream [text]` — Users post anonymously using salted hash IDs.            | ✅     |
| **Emoji reactions**         | Inline emoji reactions for community feedback.                  | ✅     |
| **Top screams of the day**   | `/top` — Displays the most upvoted screams with a meme (ImgFlip API).        | ✅     |
| **Detailed stats**          | `/stats` — Posts count, reaction count, and reaction distribution chart.    | ✅     |
| **Weekly stress graph**     | `/stress` — Community stress visualized via QuickChart.io.                  | ✅     |
| **Moderation**              | `/delete [id]` — Admins can remove inappropriate content.                   | ✅     |
| **Admin creation**          | `/create_admin [user_id]` — Promote users to admin (admin-only).            | ✅  *(New feature)* |
| **Feed browsing**           | `/feed` — Scrollable, user-friendly view of latest screams.                 | ✅  *(New feature)* |
| **Scream history**          | `/history` — Shows archive of top screams from previous weeks.               | ✅  *(New feature)* |

All additional features were proposed and accepted by the PM during planning and review sessions.

---
## 📌 Summary

All core features were fully implemented according to the original plan.  
Three new features were added to scale team participation and improve platform usability:

- `/history` – Scream archive
- `/feed` – User-friendly scream browser
- `/create_admin` – Admin management

> All changes were reviewed and approved by the PM.
---
