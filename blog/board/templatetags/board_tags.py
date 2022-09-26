from django import template
from board.models import *

register = template.Library()


@register.simple_tag()
def get_user_by_pk(user_pk):
    return User.objects.get(pk=user_pk)


@register.inclusion_tag('board/inclusion/subscription_notes.html')
def show_note_dict(user_pk):
    subsc = Subscriptions.objects.filter(user_id=user_pk)
    sub_user = []
    note_dict = {}
    for sub in subsc:
        sub_user.append(User.objects.get(pk=sub.subscriptions_id))
        notes = Note.objects.filter(creator=sub.subscriptions_id)
        for note in notes:
            author = User.objects.get(pk=note.creator.pk)
            like = Like.objects.filter(note=note).count()
            dislike = Dislike.objects.filter(note=note).count()
            note_dict[note] = (author, like, dislike)
    return {"note_dict": note_dict}


@register.inclusion_tag('board/inclusion/subscriptions.html')
def show_subscription_list(user_pk):
    user = User.objects.get(pk=user_pk)
    subscriptions = Subscriptions.objects.filter(user_id=user)
    sub_user = []
    for sub in subscriptions:
        sub_user.append(User.objects.get(pk=sub.subscriptions_id))
    return {"subscription_list": sub_user}
