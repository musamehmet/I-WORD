from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("words", views.words, name="words"),
    path("sentences", views.sentences, name="sentences"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("addword/<int:user_id>/", views.add_word, name="addword"),
    path("addsentence/<int:user_id>/", views.add_sentence, name="addsentence"), 
    path("search", views.search, name="search"),
    path('updateprofile/<int:user_id>/', views.update_user_profile, name='updateprofile'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
    path('editword/<int:word_id>/', views.edit_word, name='editword'),
    path('sentence/<int:sentence_id>/', views.sentence_detail, name='sentence_detail'),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path('change_password/', PasswordChangeView.as_view(), name='password_change'),
    path('all_words', views.all_words, name='all_words'),
    path('following_words', views.following_words, name='following_words'),
    path('my_words', views.my_words, name='my_words'),
     path('all_sentences', views.all_sentences, name='all_sentences'),
    path('following_sentences', views.following_sentences, name='following_sentences'),
    path('my_sentences', views.my_sentences, name='my_sentences'),
]