from django.db.models import Q

from board.models import User


def get_users_by_follower(followers):
    """Вернуть список пользователей с детальной информацией\n
    которые имеют связь с user в модели Follower"""
    return User.objects.filter(pk__in=followers) \
        .only('pk', 'username', 'photo', 'date_joined').order_by('username')


def get_user_by_pk(user_pk):
    return User.objects.get(pk=user_pk)


def get_users(user, search_field=""):
    """Показать список всех пользователей\n
    search_username - дополнительный параметр для фильтрации пользователей по имени ИЛИ pk"""
    if not search_field:
        return User.objects.filter(~Q(pk=user.pk)) \
            .only('pk', 'username', 'photo', 'date_joined').order_by('username')
    else:
        if search_field.isdigit():
            return User.objects.filter(~Q(pk=user.pk), Q(pk=search_field)) \
                .only('pk', 'username', 'photo', 'date_joined').order_by('username')
        else:
            return User.objects.filter(~Q(pk=user.pk), Q(username__icontains=search_field)) \
                .only('pk', 'username', 'photo', 'date_joined').order_by('username')
