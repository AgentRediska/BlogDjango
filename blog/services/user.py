from django.db.models import Q

from board.models import User


def get_users_by_follower(followers):
    """Вернуть список пользователей с детальной информацией\n
    которые имеют связь с user в модели Follower"""
    return User.objects.filter(pk__in=followers) \
        .only('pk', 'username', 'photo', 'date_joined').order_by('username')


def get_users(user, search_username: str = ""):
    """Показать список всех пользователей\n
    search_username - дополнительный параметр для фильтрации пользователей по имени"""
    if not search_username:
        return User.objects.filter(~Q(pk=user.pk)) \
            .only('pk', 'username', 'photo', 'date_joined').order_by('username')
    else:
        return User.objects.filter(~Q(pk=user.pk), username__icontains=search_username) \
            .only('pk', 'username', 'photo', 'date_joined').order_by('username')
