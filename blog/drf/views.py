from rest_framework.response import Response
import json

from drf.permissions import IsHimselfOrReadOnly
from drf.serializers import UserSerializer, NoteSerializer, UserNoteSerializer
from rest_framework import generics

from board.models import User, Note, Follower
from services import user as user_service
from services import note as note_service


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.query_params.get("username") is not None:
            queryset = user_service.get_users(self.request.user, search_field=self.request.query_params.get("username"))
        elif self.request.query_params.get("id"):
            queryset = user_service.get_users(self.request.user, search_field=self.request.query_params.get("id"))
        return queryset


class UserDetailView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsHimselfOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        result = UserNoteSerializer()
        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # print("#@#@##################################################################")
        # user_info = serializer.data
        # notes = note_service.get_user_notes(user=instance)
        # # notes_data = dict(NoteSerializer(notes, many=True).data[0])
        # print(serializer)
        # return Response(serializer.data | dict(NoteSerializer(notes, many=True).data))

    # def get_queryset(self):
    #     print("*********************")
    #     try:
    #         user = user_service.get_user_by_pk(self.kwargs['pk'])
    #         print(user)
    #         user_notes = note_service.get_user_notes(user=user)
    #         print(user_notes)
    #         queryset = list(user_notes).append(user)
    #         print(queryset)
    #         # queryset = list(chain(user, user_notes))
    #     except ObjectDoesNotExist:
    #         queryset = None
    #     return queryset


class FollowerListView(generics.ListCreateAPIView):
    queryset = Follower.objects.all()
