from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from board.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=14)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'photo', 'password']


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=5000)
    creation_date = serializers.DateTimeField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_published = serializers.BooleanField(default=True)
