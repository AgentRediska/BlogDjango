from django.db import models


class User(models.Model):
    name = models.CharField(max_length=15, null=False)
    password = models.CharField(max_length=15, null=False)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(null=False, max_length=200)
    content = models.CharField(null=False, max_length=2000)
    creation_date = models.DateTimeField(auto_now_add=True, db_index=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="note_creator")
    liked_user = models.ManyToManyField('User', through="Like", related_name="liked_user")
    disliked_user = models.ManyToManyField('User', through="Dislike", related_name="disliked_user")

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)

    def __str__(self):
        return f"user_pk: {self.user}, note_pk: {self.note}"


class Dislike(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)

    def __str__(self):
        return f"user_pk: {self.user}, note_pk: {self.note}"
