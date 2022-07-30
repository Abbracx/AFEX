from .models import ChatMessage, Profile
from django.shortcuts import redirect, render
from django.contrib.auth import login
from chat.models import Friend
from .forms import ChatMessageForm, SignUpForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "chat/index.html", context)


def detail(request, pk=None):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    rec_chats.update(seen=True)
    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user": user, "profile": profile, "chats": chats, "num":rec_chats.count()}
    return render(request, "chat/detail.html", context)


def sent_messages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data =  json.loads(request.body)
    new_chat = data['msg']
    new_chat_message =  ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)

    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

def chatNotification(request):
    user = request.user.profile 
    friends = user.friends.all()

    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr,safe=False)

def search_list_view(request):
    # query = request.POST['search']
    # print(request.body)
    user = request.user.profile
    if request.method == 'POST':
        data = json.loads(request.body)
        query = Q(profile__user__username__icontains=data) or Q(profile__name__icontains=data)
        result = list(user.friends.filter(query).values('profile__user__username'))
        print(result)
    return JsonResponse(result, safe=False)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('signIn')
    else:
        form =SignUpForm()

    return render(request, 'chat/signup.html', {'form': form})

