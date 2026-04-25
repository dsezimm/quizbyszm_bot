from django.db import models


class UserQuery(models.Model):
    """Модель для хранения всех запросов пользователей из Telegram-бота."""

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('answered', 'Отвечен'),
        ('closed', 'Закрыт'),
    ]

    COMMAND_CHOICES = [
        ('/start', 'Старт'),
        ('/help', 'Помощь'),
        ('/quiz', 'Квиз'),
        ('/score', 'Результат'),
        ('/stats', 'Статистика'),
        ('message', 'Сообщение'),
        ('answer', 'Ответ на вопрос'),
    ]

    # Данные пользователя
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Username')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Фамилия')

    # Запрос
    command = models.CharField(max_length=50, choices=COMMAND_CHOICES, default='message', verbose_name='Команда')
    message_text = models.TextField(verbose_name='Текст сообщения')

    # Ответ поддержки
    admin_reply = models.TextField(blank=True, null=True, verbose_name='Ответ администратора')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering = ['-created_at']

    def __str__(self):
        user = self.username or self.first_name or str(self.telegram_id)
        return f"{user} | {self.command} | {self.created_at.strftime('%d.%m.%Y %H:%M')}"

    def get_full_name(self):
        parts = [self.first_name, self.last_name]
        return ' '.join(p for p in parts if p) or 'Без имени'


class QuizResult(models.Model):
    """Модель для хранения результатов квизов пользователей."""

    TOPIC_CHOICES = [
        ('python', 'Python'),
        ('sql', 'SQL'),
    ]

    telegram_id = models.BigIntegerField(verbose_name='Telegram ID')
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='Username')
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, verbose_name='Тема')
    score = models.IntegerField(verbose_name='Баллы')
    total = models.IntegerField(verbose_name='Всего вопросов')
    percentage = models.FloatField(verbose_name='Процент')
    time_spent = models.FloatField(verbose_name='Время (сек)')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')

    class Meta:
        verbose_name = 'Результат квиза'
        verbose_name_plural = 'Результаты квизов'
        ordering = ['-completed_at']

    def __str__(self):
        user = self.username or str(self.telegram_id)
        return f"{user} | {self.get_topic_display()} | {self.score}/{self.total} ({self.percentage:.1f}%)"
