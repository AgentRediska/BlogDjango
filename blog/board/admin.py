from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class NoteInline(admin.TabularInline):
    model = Note
    fields = ('title', 'content', 'is_published', 'get_likes_count', 'get_dislikes_count')
    readonly_fields = ('title', 'content', 'get_likes_count', 'get_dislikes_count')
    extra = 0

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    get_likes_count.short_description = "Количество лайков"
    get_dislikes_count.short_description = "Количество дизлайков"


class SubscriptionsInline(admin.TabularInline):
    verbose_name_plural = 'Подписки'
    model = Follower
    fk_name = 'subscriber'
    readonly_fields = ('user',)
    extra = 0


class SubscribersInline(admin.TabularInline):
    verbose_name_plural = 'Подписчики'
    model = Follower
    fk_name = 'user'
    readonly_fields = ('subscriber',)
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'get_html_photo', 'date_joined')
    list_display_links = ('id', 'username')
    search_fields = ('date_joined', 'username')
    list_filter = ('date_joined',)
    fields = ('username', 'get_html_photo', 'date_joined')
    readonly_fields = ('username', 'get_html_photo', 'date_joined')
    inlines = [SubscriptionsInline, SubscribersInline, NoteInline]

    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=40>")

    get_html_photo.short_description = "Фото профиля"


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'creation_date', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'creator__username',)
    list_filter = ('creation_date', 'creator')
    list_select_related = ('creator',)
    list_editable = ('is_published',)
    readonly_fields = ('title', 'creator', 'content', 'get_likes_count',
                       'likes', 'get_dislikes_count', 'dislikes')
    fieldsets = (
        (None, {
            'fields': ('title', 'creator', 'content')
        }),
        ('Лайк / Дизлайк', {
            'classes': ('collapse',),
            'fields': ('get_likes_count', 'likes', 'get_dislikes_count', 'dislikes'),
        }),)
    save_on_top = True

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    get_likes_count.short_description = "Количество лайков"
    get_dislikes_count.short_description = "Количество дизлайков"


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)

admin.site.site_title = "Админ-панель сайта Let's tell"
admin.site.site_header = "Админ-панель сайта Let's tell"
