from django.contrib import admin
from .models import User, Word, Sentence, Follow

admin.site.register(User)
admin.site.register(Word)
admin.site.register(Sentence)
admin.site.register(Follow)