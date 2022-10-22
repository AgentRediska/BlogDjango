from django import template
from board.models import *

register = template.Library()


@register.simple_tag()
def get_user_by_pk(user_pk):
    return User.objects.get(pk=user_pk)


@register.inclusion_tag('board/inclusion/subscriptions.html')
def show_subscription_list(user_pk, search_text=''):
    user = User.objects.get(pk=user_pk)
    subscriptions = Subscription.objects.filter(user_id=user)
    sub_user = []
    for sub in subscriptions:
        user = User.objects.get(pk=sub.subscription_id)
        if search_text in user.username:
            sub_user.append(User.objects.get(pk=sub.subscription_id))
    return {"subscription_list": sub_user}


@register.inclusion_tag('board/inclusion/notes.html')
def show_notes(notes, user):
    return {'notes': notes, 'user': user}


@register.inclusion_tag('board/inclusion/notes.html')
def show_my_notes(notes, user):
    return {'notes': notes, 'user': user}
