from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UserQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('command', models.CharField(
                    choices=[('/start', 'Старт'), ('/help', 'Помощь'), ('/quiz', 'Квиз'),
                              ('/score', 'Результат'), ('/stats', 'Статистика'),
                              ('message', 'Сообщение'), ('answer', 'Ответ на вопрос')],
                    default='message', max_length=50, verbose_name='Команда'
                )),
                ('message_text', models.TextField(verbose_name='Текст сообщения')),
                ('admin_reply', models.TextField(blank=True, null=True, verbose_name='Ответ администратора')),
                ('status', models.CharField(
                    choices=[('new', 'Новый'), ('answered', 'Отвечен'), ('closed', 'Закрыт')],
                    default='new', max_length=20, verbose_name='Статус'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Запрос пользователя',
                'verbose_name_plural': 'Запросы пользователей',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(verbose_name='Telegram ID')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Username')),
                ('topic', models.CharField(
                    choices=[('python', 'Python'), ('sql', 'SQL')],
                    max_length=20, verbose_name='Тема'
                )),
                ('score', models.IntegerField(verbose_name='Баллы')),
                ('total', models.IntegerField(verbose_name='Всего вопросов')),
                ('percentage', models.FloatField(verbose_name='Процент')),
                ('time_spent', models.FloatField(verbose_name='Время (сек)')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата прохождения')),
            ],
            options={
                'verbose_name': 'Результат квиза',
                'verbose_name_plural': 'Результаты квизов',
                'ordering': ['-completed_at'],
            },
        ),
    ]
