from django import template
from board.models import *

register = template.Library()


@register.inclusion_tag('board/inclusion/subscriptions.html')
def show_subscription_list(user, search_text=''):
    if not search_text:
        subscriptions = Follower.objects.filter(subscriber=user, user__username__icontains=search_text).values('user')
    else:
        subscriptions = Follower.objects.filter(subscriber=user).values('user')
    users = User.objects.filter(pk__in=subscriptions)
    return {"subscription_list": users}


@register.inclusion_tag('board/inclusion/notes.html')
def show_notes(notes, user):
    return {'notes': notes, 'user': user}


@register.inclusion_tag('board/inclusion/notes.html')
def show_my_notes(notes, user):
    return {'notes': notes, 'user': user}
