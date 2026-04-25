import os
import sys
import json
import random
import time
import django
import telebot
from telebot import types

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quiz_django'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_django.settings')
django.setup()

from quiz_app.models import UserQuery, QuizResult

BOT_TOKEN = os.getenv('BOT_TOKEN', '8793268428:AAFPbARqJ6PcECDn5lQ8a41hvH18gKoxyg4')
bot = telebot.TeleBot(BOT_TOKEN)

sessions = {}

QUESTIONS = {
    'python': [
        {
            "question": "Какая функция используется для вывода текста в Python?",
            "options": {"A": "echo()", "B": "print()", "C": "write()", "D": "output()"},
            "answer": "B"
        },
        {
            "question": "Какой тип данных возвращает input()?",
            "options": {"A": "int", "B": "float", "C": "str", "D": "bool"},
            "answer": "C"
        },
        {
            "question": "Что делает len([1, 2, 3])?",
            "options": {"A": "Возвращает 2", "B": "Возвращает 3", "C": "Возвращает 4", "D": "Ошибка"},
            "answer": "B"
        },
        {
            "question": "Как создать пустой словарь в Python?",
            "options": {"A": "[]", "B": "()", "C": "{}", "D": "set()"},
            "answer": "C"
        },
        {
            "question": "Какой оператор используется для возведения в степень?",
            "options": {"A": "^", "B": "**", "C": "^^", "D": "pow"},
            "answer": "B"
        },
    ],
    'sql': [
        {
            "question": "Какой оператор используется для выборки данных?",
            "options": {"A": "GET", "B": "FETCH", "C": "SELECT", "D": "RETRIEVE"},
            "answer": "C"
        },
        {
            "question": "Что делает команда DELETE без WHERE?",
            "options": {"A": "Удаляет таблицу", "B": "Удаляет все строки", "C": "Ничего", "D": "Ошибка"},
            "answer": "B"
        },
        {
            "question": "Какой JOIN возвращает все строки из обеих таблиц?",
            "options": {"A": "INNER JOIN", "B": "LEFT JOIN", "C": "RIGHT JOIN", "D": "FULL OUTER JOIN"},
            "answer": "D"
        },
        {
            "question": "Что означает PRIMARY KEY?",
            "options": {
                "A": "Первая колонка",
                "B": "Уникальный идентификатор строки",
                "C": "Обязательное поле",
                "D": "Индекс"
            },
            "answer": "B"
        },
        {
            "question": "Какая функция считает количество строк?",
            "options": {"A": "SUM()", "B": "COUNT()", "C": "TOTAL()", "D": "NUM()"},
            "answer": "B"
        },
    ]
}


def save_query(message, command='message'):
    """Сохраняет запрос пользователя в базу данных Django."""
    user = message.from_user
    UserQuery.objects.create(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        command=command,
        message_text=message.text or '',
    )


def get_user_name(message):
    """Возвращает имя пользователя для отображения в боте."""
    user = message.from_user
    return user.first_name or user.username or 'пользователь'


def make_topic_keyboard():
    """Создаёт inline-клавиатуру выбора темы."""
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton('🐍 Python', callback_data='topic_python'),
        types.InlineKeyboardButton('🗄️ SQL', callback_data='topic_sql'),
    )
    return kb


def make_answer_keyboard():
    """Создаёт inline-клавиатуру вариантов ответа."""
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton('A', callback_data='ans_A'),
        types.InlineKeyboardButton('B', callback_data='ans_B'),
        types.InlineKeyboardButton('C', callback_data='ans_C'),
        types.InlineKeyboardButton('D', callback_data='ans_D'),
    )
    return kb

@bot.message_handler(commands=['start'])
def cmd_start(message):
    save_query(message, '/start')
    name = get_user_name(message)
    text = (
        f"👋 Привет, *{name}*!\n\n"
        "Я — бот для проверки знаний по программированию.\n\n"
        "📚 *Доступные команды:*\n"
        "/quiz — начать квиз\n"
        "/score — мои последние результаты\n"
        "/stats — общая статистика\n"
        "/help — помощь\n\n"
        "Нажми /quiz, чтобы начать! 🚀"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def cmd_help(message):
    save_query(message, '/help')
    text = (
        "🆘 *Помощь*\n\n"
        "Этот бот проводит квизы по программированию.\n\n"
        "*Как пользоваться:*\n"
        "1️⃣ Введи /quiz\n"
        "2️⃣ Выбери тему: Python или SQL\n"
        "3️⃣ Отвечай на вопросы кнопками A/B/C/D\n"
        "4️⃣ Получи результат!\n\n"
        "*Команды:*\n"
        "/quiz — новый квиз\n"
        "/score — последние результаты\n"
        "/stats — статистика по всем пользователям\n\n"
        "Есть вопросы? Напиши любое сообщение — "
        "администратор ответит в ближайшее время. 📩"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['quiz'])
def cmd_quiz(message):
    save_query(message, '/quiz')
    name = get_user_name(message)
    bot.send_message(
        message.chat.id,
        f"📝 *{name}*, выбери тему квиза:",
        parse_mode='Markdown',
        reply_markup=make_topic_keyboard()
    )


@bot.message_handler(commands=['score'])
def cmd_score(message):
    save_query(message, '/score')
    user_id = message.from_user.id
    results = QuizResult.objects.filter(telegram_id=user_id).order_by('-completed_at')[:5]

    if not results:
        bot.send_message(
            message.chat.id,
            "📊 У тебя пока нет результатов.\nНачни квиз командой /quiz!"
        )
        return

    lines = ["📊 *Твои последние результаты:*\n"]
    for i, r in enumerate(results, 1):
        emoji = "🏆" if r.percentage >= 80 else ("👍" if r.percentage >= 50 else "📚")
        lines.append(
            f"{i}. {emoji} *{r.get_topic_display()}* — "
            f"{r.score}/{r.total} ({r.percentage:.1f}%) | ⏱ {r.time_spent:.1f}с\n"
            f"   📅 {r.completed_at.strftime('%d.%m.%Y %H:%M')}"
        )

    bot.send_message(message.chat.id, '\n'.join(lines), parse_mode='Markdown')


@bot.message_handler(commands=['stats'])
def cmd_stats(message):
    save_query(message, '/stats')
    total_games = QuizResult.objects.count()
    total_users = QuizResult.objects.values('telegram_id').distinct().count()
    total_queries = UserQuery.objects.count()

    py_games = QuizResult.objects.filter(topic='python')
    sql_games = QuizResult.objects.filter(topic='sql')

    def avg_pct(qs):
        if not qs.exists():
            return 0
        return sum(r.percentage for r in qs) / qs.count()

    text = (
        "📈 *Общая статистика бота*\n\n"
        f"👥 Пользователей: *{total_users}*\n"
        f"🎮 Всего игр: *{total_games}*\n"
        f"💬 Всего запросов: *{total_queries}*\n\n"
        f"🐍 Python — игр: *{py_games.count()}*, средний результат: *{avg_pct(py_games):.1f}%*\n"
        f"🗄️ SQL — игр: *{sql_games.count()}*, средний результат: *{avg_pct(sql_games):.1f}%*"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')



@bot.callback_query_handler(func=lambda c: c.data.startswith('topic_'))
def handle_topic(call):
    topic = call.data.split('_')[1]  # 'python' или 'sql'
    user_id = call.from_user.id

    questions = QUESTIONS[topic].copy()
    random.shuffle(questions)

    sessions[user_id] = {
        'topic': topic,
        'questions': questions,
        'index': 0,
        'score': 0,
        'start_time': time.time(),
    }

    topic_label = '🐍 Python' if topic == 'python' else '🗄️ SQL'
    bot.edit_message_text(
        f"✅ Тема выбрана: *{topic_label}*\n\nНачинаем! Всего {len(questions)} вопросов.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown'
    )

    send_question(call.message.chat.id, user_id)


def send_question(chat_id, user_id):
    """Отправляет текущий вопрос пользователю."""
    session = sessions.get(user_id)
    if not session:
        return

    idx = session['index']
    questions = session['questions']

    if idx >= len(questions):
        finish_quiz(chat_id, user_id)
        return

    q = questions[idx]
    options_text = '\n'.join(f"*{k})* {v}" for k, v in q['options'].items())
    text = (
        f"❓ *Вопрос {idx + 1}/{len(questions)}*\n\n"
        f"{q['question']}\n\n"
        f"{options_text}"
    )
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=make_answer_keyboard())


@bot.callback_query_handler(func=lambda c: c.data.startswith('ans_'))
def handle_answer(call):
    user_id = call.from_user.id
    session = sessions.get(user_id)

    if not session:
        bot.answer_callback_query(call.id, "Начни квиз командой /quiz")
        return

    answer = call.data.split('_')[1]  # 'A', 'B', 'C' или 'D'
    idx = session['index']
    q = session['questions'][idx]
    correct = q['answer']

    UserQuery.objects.create(
        telegram_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        last_name=call.from_user.last_name,
        command='answer',
        message_text=f"Q{idx+1}: выбрал {answer}, правильно: {correct}",
    )

    if answer == correct:
        session['score'] += 1
        feedback = "✅ *Правильно!*"
        bot.answer_callback_query(call.id, "✅ Верно!")
    else:
        feedback = f"❌ *Неверно!* Правильный ответ: *{correct}*"
        bot.answer_callback_query(call.id, f"❌ Неверно! Ответ: {correct}")

    session['index'] += 1

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, feedback, parse_mode='Markdown')

    time.sleep(0.5)
    send_question(call.message.chat.id, user_id)


def finish_quiz(chat_id, user_id):
    """Завершает квиз и сохраняет результат."""
    session = sessions.pop(user_id, None)
    if not session:
        return

    score = session['score']
    total = len(session['questions'])
    topic = session['topic']
    time_spent = round(time.time() - session['start_time'], 2)
    percentage = (score / total) * 100

    username = None  # Обновляется при следующем запросе

    QuizResult.objects.create(
        telegram_id=user_id,
        username=username,
        topic=topic,
        score=score,
        total=total,
        percentage=percentage,
        time_spent=time_spent,
    )

    if percentage >= 80:
        emoji, verdict = "🏆", "Отлично!"
    elif percentage >= 50:
        emoji, verdict = "👍", "Хороший результат!"
    else:
        emoji, verdict = "📚", "Нужно ещё поучиться!"

    topic_label = '🐍 Python' if topic == 'python' else '🗄️ SQL'
    text = (
        f"{emoji} *Квиз завершён!*\n\n"
        f"📚 Тема: *{topic_label}*\n"
        f"✅ Результат: *{score}/{total}* ({percentage:.1f}%)\n"
        f"⏱ Время: *{time_spent}* сек\n\n"
        f"*{verdict}*\n\n"
        "Сыграть ещё? /quiz\n"
        "Посмотреть историю? /score"
    )
    bot.send_message(chat_id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    """Любое текстовое сообщение сохраняется как запрос в поддержку."""
    save_query(message, 'message')
    name = get_user_name(message)
    bot.send_message(
        message.chat.id,
        f"📩 *{name}*, твоё сообщение получено!\n\n"
        "Администратор рассмотрит его и ответит в ближайшее время.\n\n"
        "Хочешь пройти квиз? /quiz",
        parse_mode='Markdown'
    )

if __name__ == '__main__':
    print("🤖 Quiz Bot запущен...")
    print("📊 Логи запросов сохраняются в Django БД")
    print("🌐 Откройте http://127.0.0.1:8000/admin для просмотра")
    print("Нажмите Ctrl+C для остановки\n")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
