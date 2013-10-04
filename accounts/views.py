from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from accounts.forms import UserCreateForm, AuthenticateForm, MessagesForm
from accounts.models import Message


def index(request, auth_form=None, user_form=None):
    # User is logged in
    # Make the News Feed
    if request.user.is_authenticated():
        message_form = MessagesForm()
        user = request.user
        messages_self = Message.objects.filter(user=user.id)
        messages_friends = Message.objects.filter(user__userprofile__in=user.profile.follows.all)
        messages = messages_self | messages_friends

        return render(request, 'accounts/home.html', {
            'message_form': message_form,
            'user': request.user,
            'messages': messages,
            'next_url': '/',
        })

    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request, 'accounts/index.html', {
            'auth_form': auth_form, 'user_form': user_form,
        })


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/profile/")
    if request.method == "POST":
        user_form = UserCreateForm(data=request.POST)
        if form.is_valid():
            #user = User.objects.create_user(username=form.cleaned_data["username"],
                                            #email = form.cleaned_data["email"],
                                            #password = form.cleaned_data["password"])
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            account.name = form.cleaned_data["name"]
            account.birthday = form.cleaned_data["birthday"]
            account.save()
            return redirect('/profile/')
        else:
            return index(request, user_form=user_form)
    else:
        """user is not submitting the form, show them a blank registration form"""
        form = RegistrationForm()
        return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/profile/")

    if request.method == "POST":
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect("/")
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def newsfeed(request, message_form=None):
    """Makes up the news feed.

    Return a stream of latest 10 messages and activities from everyone a user
    follows in addition to his own messages, latest activity if any.
    For example, User1 created a new class in English.
    """
    message_form = message_form or MessagesForm
    messages = Message.objects.reverse()[:10]
    return render(request, 'accounts/newsfeed.html', {
                'message_form': message_form,
                'next_url': '/newsfeed',
                'messages': messages,
                'username': request.user.username,
    })


@login_required
def message_post(request):
    if request.method == "POST":
        message_form = MessagesForm(data=request.POST)
        next_url = request.POST.get("next_url", "/newsfeed")

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect(next_url)
        else:
            return newsfeed(request, message_form)
    return redirect('/')

def get_latest(user):
    try:
        return user.message_set.order_by('id').reverse()[0]
    except IndexError:
        return ""


@login_required
def users(request, username="", message_form=None):
    if username:
        # Show a profile
        user = get_object_or_404(username=username)
        messages = Message.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile
            return render(request, 'accounts/user.html', {'user': user, 'messages': messages, })
        return render(request, 'accounts/user.html', {'user': user, 'messages': messages, 'follow': True, })

    users = User.objects.all().annotate(message=Count('message'))

    # Usage map(function, iterable), apply function to every item and
    # return a list of the results,
    messages = map(get_latest, users)
    # the zip function returns a list of tuples with a tuple containing each
    # of the argument sequences or iterables.
    obj = zip(users, messages)

    message_form = message_form or MessagesForm()
    return render(request, 'accounts/profiles.html', {
                'obj': obj,
                'next_url': '/users/',
                'message_form': message_form,
                'username': request.user.username, })


@login_required
def follow(request):
    """Adds a user to list of followed users, to get their latest activities.

    The method has an asymmetrical approach i.e. if user1 follows user2,
    then user2 does not necessarily follow user1 back. Thus user1 gets the
    latest activites and messages of user2 however user2 may not see any
    update of user1.
    Returns the number of followed users.
    """
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')

