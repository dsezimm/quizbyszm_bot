# 🤖 Programming Quiz Bot — Этап 2

Telegram-бот для квизов по Python и SQL с Django-бэкендом.

## 📁 Структура проекта

```
quiz_bot/
├── requirements.txt          # Зависимости
├── bot/
│   └── bot.py                # Telegram-бот (pyTelegramBotAPI)
└── quiz_django/
    ├── manage.py             # Django CLI
    ├── quiz_django/          # Настройки Django
    │   ├── settings.py
    │   └── urls.py
    └── quiz_app/             # Django приложение
        ├── models.py         # Модели: UserQuery, QuizResult
        └── admin.py          # Настройка админ-панели
```

## 🚀 Установка и запуск

### 1. Установить зависимости
```bash
pip install -r requirements.txt
```

### 2. Применить миграции Django
```bash
cd quiz_django
python manage.py makemigrations quiz_app
python manage.py migrate
```

### 3. Создать суперпользователя для админки
```bash
python manage.py createsuperuser
```

### 4. Запустить Django-сервер (в одном терминале)
```bash
python manage.py runserver
```

### 5. Вставить токен бота и запустить (в другом терминале)
Открыть `bot/bot.py` и заменить:
```python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```
на токен от [@BotFather](https://t.me/BotFather).

```bash
cd bot
BOT_TOKEN=ваш_токен python bot.py
```

## 🌐 Админ-панель

Открыть: http://127.0.0.1:8000/admin

- **Запросы пользователей** — все сообщения из бота, фильтрация по статусу
- **Результаты квизов** — история прохождений с процентами
- Поддержка: заполните поле "Ответ администратора" и смените статус на "Отвечен"

## 📋 Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие и список команд |
| `/help` | Подробная помощь |
| `/quiz` | Начать квиз (выбор темы) |
| `/score` | Последние 5 результатов |
| `/stats` | Общая статистика бота |
| любое сообщение | Запрос в поддержку |

## 🗄️ Модели Django

### UserQuery
Сохраняет каждый запрос пользователя:
- `telegram_id`, `username`, `first_name`, `last_name`
- `command` — тип команды (`/start`, `/quiz`, `message`, `answer`, ...)
- `message_text` — текст сообщения
- `admin_reply` — ответ поддержки
- `status` — новый / отвечен / закрыт
- `created_at`, `updated_at`

### QuizResult
Итоги каждого пройденного квиза:
- `telegram_id`, `username`
- `topic` — python / sql
- `score`, `total`, `percentage`
- `time_spent`
- `completed_at`
