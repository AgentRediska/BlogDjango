from board.models import Follower, User


def get_subscriptions(user, subscription_name: str = ""):
    """Найти подписки. Subscription_name - дополнительная фильтрация по имени"""
    if not subscription_name:
        return Follower.objects.filter(subscriber=user).values('user')
    else:
        return Follower.objects.filter(subscriber=user,
                                       user__username__icontains=subscription_name).values('user')


def get_subscribers(user, subscriber_name: str = ""):
    """Найти подписчиков. Subscriber_name - дополнительная фильтрация по имени"""
    if not subscriber_name:
        return Follower.objects.filter(user=user).values('subscriber')
    else:
        return Follower.objects.filter(user=user, subscriber__username__icontains=subscriber_name).values('subscriber')


def unsubscribe(user, sub_pk):
    """Отписаться от пользователя"""
    return Follower.objects.filter(subscriber=user, user=User.objects.get(pk=sub_pk)).delete()


def subscribe(user, sub_pk):
    """Подписаться на пользователя"""
    return Follower.objects.create(user=User.objects.get(pk=sub_pk), subscriber=user)


def exclude_user_from_subscriptions(user, sub_pk):
    """Исключить пользователя из списка подписчиков"""
    Follower.objects.filter(subscriber=User.objects.get(pk=sub_pk), user=user).delete()


def is_subscription(speaker, user):
    """Проверить подписку"""
    return Follower.objects.filter(user=user, subscriber=speaker).exists()


def is_subscriber(user, speaker):
    """Проверить наличие подписки у пользователя"""
    return Follower.objects.filter(user=speaker, subscriber=user).exists()


def check_user_relationship(user, speaker) -> list:
    """Проверить связь между пользователями\n
    list[0] - пользователь подписан на user-a,\n
    list[1] - user подписан на пользователя"""
    return [is_subscriber(user, speaker), is_subscription(speaker, user)]
