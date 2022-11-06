from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from board.models import User, Note
from drf.serializers import UserSerializer, NoteSerializer


class UserAPIView(APIView):
    def get(self, request):
        user_list = User.objects.all().values()
        return Response({'users': list(user_list)})

    def post(self, request):
        post_user = User.objects.create(
            username=request.data['username'],
            password=request.data['password'],
        )
        return Response({'post': model_to_dict(post_user)})


class NoteAPIView(APIView):
    def get(self, request):
        return Response({'notes': NoteSerializer(Note.objects.all(), many=True).data})

    def post(self, request):
        note = Note.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            creator=request.user,
            is_published=request.data['is_published']
        )
        return Response({'post': NoteSerializer(note).data})
