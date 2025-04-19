# InnoScream – Anonymous Student Scream Platform (Bot)

A Telegram-integrated platform where students can anonymously share their academic frustrations, support each other with reactions, and get memes + weekly analytics.

---

## ⚙️ Tech Stack

- **Bot:** Python 3.11, aiogram (Telegram), httpx, asyncio
- **External APIs:**  
  - 📊 [InnoScreamAPI](https://github.com/creepydanunity/InnoScream/tree/api)

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/creepydanunity/innoscream.git
cd innoscream
git checkout bot
```

### 2. Set up virtual environment (recommended via Poetry)

```bash
poetry install
```

### 3. Create `.env` file in `app_bot/`

```env
BOT_TOKEN=<TelegramAPI_Token>
API_URL=<InnoScreamAPI_URL>
```

## 🚀 Running the Project
### Start the bot:
```bash
poetry run python -m app_bot.main
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