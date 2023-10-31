from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

class User(AbstractUser):
    biography = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    profileURL = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    wordscore = models.IntegerField(default=0, blank=True)
    sentencescore = models.IntegerField(default=0, blank=True)
    darkmode = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_word')
    word = models.CharField(max_length=255, unique=True, default='')
    description = models.CharField(max_length=1024, default='')
    pronunciation = models.CharField(max_length=255, default='')
    prontype = models.CharField(max_length=255, default='')
    type = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.word

class Sentence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_sentence')
    sentenceword = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='sentence_word', null=False)
    sentence = models.CharField(max_length=2048, default='')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.sentence
    
class Follow(models.Model):
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_is_being_followed")

    def __str__(self):
        return f"{self.user_follower} is following {self.user_followed}"