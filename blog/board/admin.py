from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'creation_date')
    list_display_links = ('pk', 'name')
    search_fields = ('pk', 'name')
    list_filter = ('creation_date',)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'creation_date')
    list_display_links = ('title', 'creator')
    search_fields = ('title', 'creator__name',)
    list_filter = ('creation_date', 'creator')


admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
