# 🤖 Programming Quiz Bot

A Telegram bot for testing knowledge in **Python** and **SQL**, built with `pyTelegramBotAPI` and `Django`.

> 📚 Academic project — Stage 2

---

## ✨ Features

- Interactive quiz with **5 questions** per topic (Python or SQL)
- Inline buttons for topic selection and answering (A / B / C / D)
- Every user request is saved to a **Django database**
- **Django Admin panel** to view all requests and reply to users
- Quiz results stored with score, percentage, and time spent

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pyTelegramBotAPI` | Telegram Bot API integration |
| `Django 4.2` | Backend + ORM + Admin panel |
| `SQLite` | Database |
| `Python 3.x` | Main language |

---

## 📁 Project Structure

```
quiz_bot/
├── requirements.txt
├── README.md
├── bot/
│   └── bot.py              # Telegram bot logic
└── quiz_django/
    ├── manage.py
    ├── quiz_django/
    │   ├── settings.py
    │   └── urls.py
    └── quiz_app/
        ├── models.py       # UserQuery, QuizResult models
        ├── admin.py        # Admin panel configuration
        └── migrations/
```

---

## 🗄️ Database Models

### `UserQuery`
Stores every message sent to the bot:

| Field | Description |
|-------|-------------|
| `telegram_id` | User's Telegram ID |
| `username` | Telegram username |
| `command` | Command used (`/start`, `/quiz`, etc.) |
| `message_text` | Full message text |
| `admin_reply` | Support reply from admin |
| `status` | `new` / `answered` / `closed` |
| `created_at` | Timestamp |

### `QuizResult`
Stores quiz results:

| Field | Description |
|-------|-------------|
| `topic` | `python` or `sql` |
| `score` | Correct answers |
| `total` | Total questions |
| `percentage` | Score percentage |
| `time_spent` | Time in seconds |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/dsezimm/quiz-bot.git
cd quiz-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations
```bash
cd quiz_django
python manage.py migrate
```

### 4. Create admin user
```bash
python manage.py createsuperuser
```

### 5. Add your bot token
Open `bot/bot.py` and replace:
```python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```
Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

### 6. Run Django server (Terminal 1)
```bash
python manage.py runserver
```

### 7. Run the bot (Terminal 2)
```bash
cd bot
python bot.py
```

---

## 💬 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message |
| `/help` | Help and instructions |
| `/quiz` | Start a new quiz |
| `/score` | View your last 5 results |
| `/stats` | Global bot statistics |
| any message | Saved as support request |

---

## 🌐 Admin Panel

Open in browser: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

- View all user requests with filters by status and command
- Reply to user questions via `admin_reply` field
- Track quiz results with visual percentage bars

---

## 👤 Author

**dsezimm** — [github.com/dsezimm](https://github.com/dsezimm)
