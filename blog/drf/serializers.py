from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from board.models import User, Note, Follower


class NoteSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=5000)
    creation_date = serializers.DateTimeField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_published = serializers.BooleanField(default=True)

    class Meta:
        model = Note
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=14)
    password = serializers.CharField(min_length=8, write_only=True)
    note_creator = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'photo', 'password', 'note_creator']


class UserNoteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    notes = NoteSerializer(many=True)

    class Meta:
        model = User
        fields = ['user', 'notes']


class FollowerSerializer(serializers.ModelSerializer):
    subscriber = UserSerializer(many=True)

    class Meta:
        model = Follower
        fields = ['subscriber', 'subscriber']


class UserUserSerializer(serializers.ModelSerializer):
    follower = FollowerSerializer(many=True)

    class Meta:
        model = User
        fields = ['follower']
