from django.contrib import admin
from django.utils.html import format_html
from .models import UserQuery, QuizResult


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_display', 'telegram_id', 'command',
        'short_message', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'command', 'created_at']
    search_fields = ['telegram_id', 'username', 'first_name', 'message_text']
    readonly_fields = ['telegram_id', 'username', 'first_name', 'last_name',
                       'command', 'message_text', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('👤 Данные пользователя', {
            'fields': ('telegram_id', 'username', 'first_name', 'last_name')
        }),
        ('💬 Запрос', {
            'fields': ('command', 'message_text', 'created_at')
        }),
        ('✉️ Ответ поддержки', {
            'fields': ('status', 'admin_reply', 'updated_at'),
            'description': 'Заполните поле ниже, чтобы ответить на вопрос пользователя.'
        }),
    )

    def get_user_display(self, obj):
        name = obj.get_full_name()
        if obj.username:
            return format_html('<b>{}</b> <span style="color:gray">@{}</span>', name, obj.username)
        return format_html('<b>{}</b>', name)
    get_user_display.short_description = 'Пользователь'

    def short_message(self, obj):
        text = obj.message_text
        if len(text) > 60:
            return text[:60] + '...'
        return text
    short_message.short_description = 'Сообщение'

    def status_badge(self, obj):
        colors = {
            'new': '#e74c3c',
            'answered': '#27ae60',
            'closed': '#95a5a6',
        }
        labels = {
            'new': '🔴 Новый',
            'answered': '🟢 Отвечен',
            'closed': '⚫ Закрыт',
        }
        color = colors.get(obj.status, '#333')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Статус'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_display', 'topic', 'score_display',
        'percentage_bar', 'time_spent_display', 'completed_at'
    ]
    list_filter = ['topic', 'completed_at']
    search_fields = ['telegram_id', 'username']
    readonly_fields = ['telegram_id', 'username', 'topic', 'score',
                       'total', 'percentage', 'time_spent', 'completed_at']
    ordering = ['-completed_at']
    date_hierarchy = 'completed_at'

    def get_user_display(self, obj):
        if obj.username:
            return format_html('@{}', obj.username)
        return str(obj.telegram_id)
    get_user_display.short_description = 'Пользователь'

    def score_display(self, obj):
        return format_html('<b>{}/{}</b>', obj.score, obj.total)
    score_display.short_description = 'Результат'

    def percentage_bar(self, obj):
        pct = obj.percentage
        if pct >= 80:
            color = '#27ae60'
        elif pct >= 50:
            color = '#f39c12'
        else:
            color = '#e74c3c'
        return format_html(
            '<div style="width:100px; background:#eee; border-radius:4px;">'
            '<div style="width:{:.0f}px; background:{}; border-radius:4px; text-align:center; color:white; font-size:11px;">{:.1f}%</div>'
            '</div>',
            pct, color, pct
        )
    percentage_bar.short_description = 'Процент'

    def time_spent_display(self, obj):
        return f"{obj.time_spent:.1f} сек"
    time_spent_display.short_description = 'Время'


# Настройка заголовка админ-панели
admin.site.site_header = '🤖 Programming Quiz Bot — Панель управления'
admin.site.site_title = 'Quiz Bot Admin'
admin.site.index_title = 'Управление ботом'
