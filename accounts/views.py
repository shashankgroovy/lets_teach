from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models. import Count
from django.core.exceptions import ObjectDoesNotExist

from accounts.forms import UserCreationForm, AuthenticationForm, MessagesForm
from accounts.models import Messages


def index(request, auth_form=None, user_form=None):
    # User is logged in
    # Make the News Feed
    if request.user.is_authenticated():
        message_form = MessageForm()
        user = request.user
        messages_self = Messages.objects.filter(user=user.id)
        messages_friends = Messages.objects.filter(user__userprofile__in=user.profile.follows.all)
        messages = messages_self | messages_friends

        return render(request, 'accounts/home.html', {
            'mesage_form': message_form,
            'user':, request.user,
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
        else:')
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
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            account = authenticate(username=username, password=password)
            if account is not None:
                login(request, account)
                return HttpResponseRedirect("/profile/")
            else:
                return render_to_response("login.html", {"form": form}, context_instance=RequestContext(request))
        else:
            return render_to_response("login.html", {"form": form}, context_instance=RequestContext(request))
    else:
        """user is not submitting the form, show the login form"""
        form = LoginForm()
        context = {"form": form}
        return render_to_response("login.html", context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect("/")
