from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import generics
from drf.permissions import IsHimselfOrReadOnly, IsNoteCreatorOrReadOnly
from drf.serializers import NoteSerializer, UserFollowerSerializer, UserBaseInfoSerializer
from drf.paginations import *

from board.models import User, Note
from services import user as user_s
from services import note as note_s
from services import follower as follower_s


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserBaseInfoSerializer
    pagination_class = UsersPagination

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.query_params.get("username") is not None:
            queryset = user_s.get_users(self.request.user, search_field=self.request.query_params.get("username"))
        elif self.request.query_params.get("id"):
            queryset = user_s.get_users(self.request.user, search_field=self.request.query_params.get("id"))
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowerSerializer
    permission_classes = (IsHimselfOrReadOnly,)


class FollowerListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowerSerializer
    pagination_class = UsersPagination


class FollowerDetailView(generics.RetrieveDestroyAPIView,
                         generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        sub_pk = self.kwargs.get("pk")
        if not follower_s.is_subscriber(user, sub_pk):
            follower_s.subscribe(user, sub_pk)
            return Response({"message": "You have subscribed to a user"})
        else:
            return Response({"message": "You are already following a user"})

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        sub_pk = self.kwargs.get("pk")
        if follower_s.is_subscriber(user, sub_pk):
            follower_s.unsubscribe(user, sub_pk)
            return Response({"message": "You have unsubscribed from the user"})
        else:
            return Response({"message": "You are not following a user"})


class SubscriptionNoteListView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = NotesPagination

    def get_queryset(self):
        return note_s.get_notes_user_subscriptions(self.request.user)


class UserNoteListView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = NotesPagination

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        return note_s.get_all_user_notes(self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsNoteCreatorOrReadOnly,)


class NoteLikeView(generics.CreateAPIView,
                   generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        result = note_s.set_like(self.request.user, self.kwargs.get("pk"))
        if result:
            return Response({"result": True})
        else:
            return Response({"result": "Like already placed"})

    def delete(self, request, *args, **kwargs):
        result = note_s.delete_like(self.request.user, self.kwargs.get("pk"))
        if result:
            return Response({"result": True})
        else:
            return Response({"result": "Like not found"})


class NoteDislikeView(generics.CreateAPIView,
                      generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        result = note_s.set_dislike(self.request.user, self.kwargs.get("pk"))
        if result:
            return Response({"result": True})
        else:
            return Response({"result": "Dislike already placed"})

    def delete(self, request, *args, **kwargs):
        result = note_s.delete_dislike(self.request.user, self.kwargs.get("pk"))
        if result:
            return Response({"result": True})
        else:
            return Response({"result": "Dislike not found"})
