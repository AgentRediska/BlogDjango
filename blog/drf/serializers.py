from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from board.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=5000)
    creation_date = serializers.DateTimeField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_published = serializers.BooleanField(default=True)


# class NoteModel:
#     def __init__(self, title, content, is_published):
#         self.title = title
#         self.content = content
#         self.is_published = is_published
#
#
# class NoteSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     content = serializers.CharField(max_length=5000)
#     is_published = serializers.BooleanField(default=True)
#
#
# def encode():
#     model = NoteModel("title", "content", True)
#     model_sr = NoteSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
