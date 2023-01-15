from django.contrib.auth.hashers import make_password
from drf.permissions import IsHimselfOrReadOnly
from drf.serializers import UserSerializer, NoteSerializer
from rest_framework import generics

from board.models import User, Note, Follower
from services import user as user_service


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        hashed_password = make_password(serializer.validated_data['password'])  # get the hashed password
        serializer.validated_data['password'] = hashed_password
        user = super(UserListView, self).perform_create(serializer)

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.query_params.get("username") is not None:
            queryset = user_service.get_users(self.request.user, search_field=self.request.query_params.get("username"))
        elif self.request.query_params.get("id"):
            queryset = user_service.get_users(self.request.user, search_field=self.request.query_params.get("id"))
        return queryset


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsHimselfOrReadOnly,)

    def perform_update(self, serializer):
        hashed_password = make_password(serializer.validated_data['password'])
        serializer.validated_data['password'] = hashed_password
        user = super(UserDetailView, self).perform_update(serializer)

# class UserAPIView(APIView):
#     def get(self, request):
#         user_list = User.objects.all().values()
#         return Response({'users': list(user_list)})
#
#     def post(self, request):
#         post_user = User.objects.create(
#             username=request.data['username'],
#             password=request.data['password'],
#         )
#         return Response({'post': model_to_dict(post_user)})
#
#
# class NoteAPIView(APIView):
#     def get(self, request):
#         if request.data['note_id'] is not None:
#             notes = Note.objects.get(pk=request.data['note_id'], is_published=True)
#             serializer = NoteSerializer(data=notes)
#             serializer.is_valid(raise_exception=True)
#             return Response({'notes': NoteSerializer(notes).data})
#         else:
#             if request.data['user_id'] is not None:
#                 notes = Note.objects.get(creator=request.data['user_id'], is_published=True).oreder_by('creation_date')
#             else:
#                 subscriptions = Follower.objects.filter(subscriber=self.request.user).values('user')
#                 notes = Note.objects.filter(creator__in=subscriptions, is_published=True).order_by('creation_date')
#             serializer = NoteSerializer(data=notes, many=True)
#             serializer.is_valid(raise_exception=True)
#             return Response({'notes': NoteSerializer(notes, many=True).data})
#
#
# class UsersNoteAPIView(APIView):
#     def get(self, request):
#         if request.data['note_id']:
#             note = Note.objects.get(creator=request.user, pk=request.data['note_id'])
#             serializer = NoteSerializer(data=note)
#             serializer.is_valid(raise_exception=True)
#             return Response({'notes': NoteSerializer(note).data})
#         else:
#             if request.data['is_published'] is True:
#                 notes = Note.objects.get(creator=request.user, is_published=True)
#             else:
#                 notes = Note.objects.get(creator=request.user, is_published=False)
#             serializer = NoteSerializer(data=notes)
#             serializer.is_valid(raise_exception=True)
#             return Response({'notes': NoteSerializer(notes, many=True).data})
#
#     def post(self, request):
#         serializer = NoteSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         note = Note.objects.get(pk=request.data["note_id"])
#         note.title = request.data['title'],
#         note.content = request.data['content'],
#         note.is_published = request.data['is_published']
#         note.save()
#         return Response({'updated_note': NoteSerializer(note).data})
