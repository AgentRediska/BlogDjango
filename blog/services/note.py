from django.utils.functional import SimpleLazyObject

from board.models import Note, Follower


def set_like_to_note(user, note_pk):
    """Поставить / убрать лайк из записи"""
    note = Note.objects.get(pk=note_pk)
    if note.likes.filter(id=user.pk).exists():
        note.likes.remove(user)
    else:
        if note.dislikes.filter(id=user.pk).exists():
            note.dislikes.remove(user)
        note.likes.add(user)


def set_dislike_to_note(user, note_pk):
    """Поставить / убрать дизлайк из записи"""
    note = Note.objects.get(pk=note_pk)
    if note.dislikes.filter(id=user.pk).exists():
        note.dislikes.remove(user)
    else:
        if note.likes.filter(id=user.pk).exists():
            note.likes.remove(user)
        note.dislikes.add(user)


def get_subscription_notes(subscriptions: list):
    """Вернуть все записи пользователей из подписки"""
    return Note.objects.filter(creator__in=subscriptions, is_published=True).order_by('creation_date')


def get_user_notes(user):
    """Вернуть все записи выбранного пользователя"""
    return Note.objects.filter(creator=user, is_published=True)


def get_user_draft_notes(user: SimpleLazyObject):
    """Вернуть неопубликованные записи авторизированного пользователя"""
    return Note.objects.filter(creator=user, is_published=False)


def get_notes_user_subscriptions(user):
    """Вернуть все записи пользователей из подписки"""
    subscriptions = Follower.objects.filter(subscriber=user).values('user')
    return Note.objects.filter(creator__in=subscriptions, is_published=True).order_by('creation_date')
