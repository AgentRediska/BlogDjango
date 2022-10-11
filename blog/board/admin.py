from django.contrib import admin

from .models import *


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'date_joined')
    list_display_links = ('id', 'username')
    search_fields = ('date_joined', 'username')
    list_filter = ('date_joined',)
    inlines = [SubscriptionInline]


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'creation_date')
    list_display_links = ('title', 'creator')
    search_fields = ('title', 'creator__name',)
    list_filter = ('creation_date', 'creator')


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
