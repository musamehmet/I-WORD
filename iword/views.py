from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Sentence, User, Word, Follow
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    latest_words = Word.objects.all().order_by('-id')[:10]
    words = Word.objects.all()
    sentences_count = Sentence.objects.count()
    words_count = Word.objects.count()
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    sentences_count_today = Sentence.objects.filter(created_at__gte=today_start).count()
    words_count_today = Word.objects.filter(created_at__gte=today_start).count()
    latest_sentences = Sentence.objects.all().order_by('-id')[:10]
    return render(request, "index.html", {
        "latest_words": latest_words,
        "words": words,
        "latest_sentences": latest_sentences,
        "sentences_count": sentences_count,
        "sentences_count_today": sentences_count_today,
        "words_count_today": words_count_today,
        "words_count": words_count,
    })
    
def login_view(request):        
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        location = request.POST["location"]
        biography = request.POST["biography"]
        profileURL = request.POST["profileURL"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        if not birthday:
            birthday = None
        if not profileURL:
            profileURL = f"https://randomuser.me/api/portraits/lego/1.jpg"
        try:
            user = User.objects.create_user(username=username, email=email, password=password, birthday=birthday, location=location, biography=biography, profileURL=profileURL)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": f"{username} has already been taken, please try another username."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def add_word(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    words = Word.objects.all()
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    sentences_count = Sentence.objects.count()
    words_count = Word.objects.count()
    sentences_count_today = Sentence.objects.filter(created_at__gte=today_start).count()
    words_count_today = Word.objects.filter(created_at__gte=today_start).count()
    errormessage = ""
    successmessage = ""
    new_word = None

    if request.method == "POST":
        word = request.POST["word"]
        if not word.strip():
            errormessage = "Word area can't be empty."
        else:
            description = request.POST.get("description")
            pronunciation = request.POST.get("pronunciation")
            prontype = request.POST.get("prontype")

            type = request.POST["type"]
            try:
                new_word = Word.objects.create(
                    user=request.user,
                    word=word,
                    description=description,
                    pronunciation=pronunciation,
                    prontype=prontype,
                    type=type
                )
                addscore = 25 
                user.wordscore += addscore
                user.save()
                successmessage = f"You saved {word} successfully and you earned {addscore} points for this word."
            except IntegrityError:
                errormessage = f"{word} has already been saved, please try another word."
                context = {
                "latest_sentences": Sentence.objects.all().order_by('-id')[:10],
                "latest_words": Word.objects.all().order_by('-id')[:10],
                "words": words,
                "errormessage": errormessage,
                "successmessage": successmessage,
                "sentences_count": sentences_count,
                "words_count": words_count,
                "sentences_count_today": sentences_count_today,
                "words_count_today": words_count_today,

                }
                return render(request, "index.html", context)                

    context = {
        "latest_sentences": Sentence.objects.all().order_by('-id')[:10],
        "latest_words": Word.objects.all().order_by('-id')[:10],
        "words": words,
        "errormessage": errormessage,
        "successmessage": successmessage,
    }
    if new_word:
        return redirect('word_detail', word_id=new_word.id)       
    return render(request, "index.html", context)

def word_detail(request, word_id):
    words = Word.objects.all()
    word = get_object_or_404(Word, pk=word_id)
    sentences = Sentence.objects.filter(sentenceword=word_id).order_by('-id')[:10]
    return render(request, 'word.html', {'word': word, 'sentences': sentences, 'words':words})

def sentences(request):
    all_sentences = Sentence.objects.all().order_by('-id')
    paginator = Paginator(all_sentences, 20)
    page_number = request.GET.get('page')
    sentences = paginator.get_page(page_number)
    return render(request, 'sentences.html', {'sentences': sentences})

def all_sentences(request):
    sentences = Sentence.objects.all().order_by('-id')
    paginator = Paginator(sentences, 20)
    page_number = request.GET.get('page')
    sentences = paginator.get_page(page_number)
    return render(request, 'sentences.html', {'sentences': sentences})

def following_sentences(request):
    currentUser = get_object_or_404(User, username=request.user.username)
    followed_users = Follow.objects.filter(user_follower=currentUser).values_list('user_followed', flat=True)
    sentences = Sentence.objects.filter(user__in=followed_users).order_by('-id')
    paginator = Paginator(sentences, 20)
    page_number = request.GET.get('page')
    sentences = paginator.get_page(page_number)
    return render(request, 'sentences.html', {'sentences': sentences})

def my_sentences(request):
    currentUser = get_object_or_404(User, username=request.user.username)
    sentences = Sentence.objects.filter(user=currentUser).order_by('-id')
    paginator = Paginator(sentences, 20)
    page_number = request.GET.get('page')
    sentences = paginator.get_page(page_number)
    return render(request, 'sentences.html', {'sentences': sentences})

@login_required
def add_sentence(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    words = Word.objects.all()
    errormessage = ""
    successmessage = ""
    sentence = None    
    if request.method == "POST":
        sentence = request.POST["sentence"]
        sentenceword_id = request.POST.get("sentenceword")        
        if not sentence.strip():
            errormessage = "Sentence area can't be empty."
        else:
            try:
                sentenceword = get_object_or_404(Word, pk=sentenceword_id)
                usercheck = Sentence.objects.filter(user=user, sentenceword=sentenceword).exists()
                if not usercheck:
                    addscore = 50
                    user.sentencescore += addscore
                    user.save()
                sentence = Sentence.objects.create(
                    user=user,
                    sentence=sentence,
                    sentenceword=sentenceword,
                )
                sentence.save()                
                successmessage = f"You saved {sentence.sentence} as a sentence successfully." 
                return redirect('sentence_detail', sentence_id=sentence.id) 
            except IntegrityError:
                errormessage = "System error."
    
    latest_sentences = Sentence.objects.all().order_by('-id')[:10]
    latest_words = Word.objects.all().order_by('-id')[:10]
    sentence_list = Sentence.objects.all().order_by('-id')    
    context = {
        "latest_sentences": latest_sentences, 
        "latest_words": latest_words, 
        "words": words, 
        "errormessage": errormessage, 
        "successmessage": successmessage,
        'sentence_list': sentence_list,
    }        
    if errormessage:
        messages.error(request, errormessage)
    else:
        messages.success(request, successmessage)    
    return render(request, "index.html", context)


def sentence_detail(request, sentence_id):
    sentence = get_object_or_404(Sentence, pk=sentence_id)
    sentences = Sentence.objects.filter(sentenceword=sentence_id).order_by('-id')[:10]
    sentenceword = sentence.sentenceword
    return render(request, 'sentence.html', {'sentences': sentences, 'sentence': sentence, 'sentenceword': sentenceword})
    
     
def words(request):
    all_words = Word.objects.all().order_by('-id')
    paginator = Paginator(all_words, 20)
    page_number = request.GET.get('page')
    words = paginator.get_page(page_number)
    return render(request, 'words.html', {'words': words})

def all_words(request):
    words = Word.objects.all().order_by('-id')
    paginator = Paginator(words, 20)
    page_number = request.GET.get('page')
    words = paginator.get_page(page_number)
    return render(request, 'words.html', {'words': words})

def following_words(request):
    currentUser = get_object_or_404(User, username=request.user.username)
    followed_users = Follow.objects.filter(user_follower=currentUser).values_list('user_followed', flat=True)
    words = Word.objects.filter(user__in=followed_users).order_by('-id')
    paginator = Paginator(words, 20)
    page_number = request.GET.get('page')
    words = paginator.get_page(page_number)
    return render(request, 'words.html', {'words': words})

def my_words(request):
    currentUser = get_object_or_404(User, username=request.user.username)
    words = Word.objects.filter(user=currentUser).order_by('-id')
    paginator = Paginator(words, 20)
    page_number = request.GET.get('page')
    words = paginator.get_page(page_number)
    return render(request, 'words.html', {'words': words})

def leaderboard(request):
    scorelist = User.objects.all()
    user_list = []
    for user in scorelist:
        wordscore = user.wordscore if hasattr(user, 'wordscore') else 0
        sentencescore = user.sentencescore if hasattr(user, 'sentencescore') else 0
        profilescore = int((wordscore * 30) / 100 + (sentencescore * 70) / 100)
        user.profilescore = profilescore
        user_list.append(user)
    user_list = sorted(user_list, key=lambda user: user.profilescore, reverse=True)
    for rank, user in enumerate(user_list, start=1):
        user.rank = rank
    paginator = Paginator(user_list, 20)
    page_number = request.GET.get('page')
    ranked_users = paginator.get_page(page_number)
    return render(request, 'leaderboard.html', {'ranked_users': ranked_users})

def search(request):
    query = request.GET.get('query')
    words = Word.objects.filter(word__icontains=query)    
    message = f"{query} does not exists." if not words else ""    
    return render(request, 'search.html', {'words': words, 'query': query, 'message': message})

def word_page(request, word_id):
    word = Word.objects.get(id=word_id)
    return render(request, 'word.html', {'word': word})

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    wordscore = user.wordscore if hasattr(user, 'wordscore') else 0
    sentencescore = user.sentencescore if hasattr(user, 'sentencescore') else 0
    profilescore = int((wordscore * 30) / 100 + (sentencescore * 70) / 100)
    following = Follow.objects.filter(user_follower=user_id)
    followers = Follow.objects.filter(user_followed=user_id)
    isFollowing = Follow.objects.filter(user_follower=request.user, user_followed=user).exists()
    latest_words = Word.objects.filter(user=user_id).order_by('-id')[:10]
    latest_sentences = Sentence.objects.filter(user=user_id).order_by('-id')[:10]
    scorelist = User.objects.all()
    user_list = []
    for u in scorelist:
        w_score = u.wordscore if hasattr(u, 'wordscore') else 0
        s_score = u.sentencescore if hasattr(u, 'sentencescore') else 0
        rank_score = int((w_score * 30) / 100 + (s_score * 70) / 100)
        u.rank_score = rank_score
        user_list.append(u)
    user_list = sorted(user_list, key=lambda u: u.rank_score, reverse=True)
    for rank, u in enumerate(user_list, start=1):
        if u == user:
            user.rank = rank
            break
    return render(request, "profile.html", {
        "user": user,
        "wordscore": wordscore,
        "sentencescore": sentencescore,
        "profilescore": profilescore,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "latest_words": latest_words,
        "latest_sentences": latest_sentences,
        "rank": user.rank
    })

@login_required
def update_user_profile(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.biography = request.POST['biography']
        user.profileURL = request.POST['profileURL']
        user.location = request.POST['location']        
        if 'birthday' in request.POST:
            birthday = request.POST['birthday']
            if birthday:  
                user.birthday = birthday        
        if not user.profileURL:
            user.profileURL = f"https://randomuser.me/api/portraits/lego/1.jpg"        
        user.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('profile', user_id)
    return render(request, 'profile.html')

@login_required
def edit_word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    sentences = Sentence.objects.filter(sentenceword=word_id).order_by('-id')[:10]    
    if request.method == "POST":
        new_word = request.POST.get("word")
        new_description = request.POST.get("description")
        new_pronunciation = request.POST.get("pronunciation")
        new_prontype = request.POST.get("prontype")
        new_type = request.POST.get("type")        
    try:
        word.word = new_word
        word.description = new_description
        word.pronunciation = new_pronunciation
        word.prontype = new_prontype
        word.type = new_type
        word.save()
        messages.success(request, "Word updated successfully.")
        return render(request, 'word.html', {'word': word, 'sentences': sentences, 'words':words})    
    except IntegrityError:
                errormessage = "System error."
    return render(request, "word.html", {"word": word, "sentences": sentences})

def follow(request):
    userfollow = request.POST.get('userfollow')
    currentUser = get_object_or_404(User, username=request.user.username)
    userfollowData = get_object_or_404(User, pk=userfollow)
    f = Follow(user_follower=currentUser, user_followed=userfollowData)
    f.save()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))

def unfollow(request):
    userfollow = request.POST.get('userfollow') 
    currentUser = get_object_or_404(User, username=request.user.username)
    userfollowData = get_object_or_404(User, pk=userfollow)
    f = Follow.objects.get(user_follower=currentUser, user_followed=userfollowData)
    f.delete()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))
