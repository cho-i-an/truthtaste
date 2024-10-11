from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login

from actions.models import Action
from users.forms import UserProfileForm


def profile(request, username):

    if not request.session.get("username"):
        messages.error(request, "You need to log in to view this page.")
        return redirect('truthtaste:home')

    viewed_user = get_object_or_404(User, username=username)
    current_user = request.user

    editable = (current_user.details.role == 'admin') or (current_user == viewed_user)

    email_subscribe_initial = 'Yes' if viewed_user.details.email_subscribe else 'No'
    user_role = viewed_user.details.role

    if request.method == 'POST' and editable:
        form = UserProfileForm(request.POST, instance=viewed_user, user_role=current_user.details.role)
        if form.is_valid():
            new_password = form.cleaned_data.get("password")
            form.save()
            if new_password:
                logout(request)
            messages.success(request, "Profile updated successfully. Please log in again.")
            return redirect('truthtaste:home')
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Invalid form content")
            return redirect('truthtaste:home')
    else:
        form = UserProfileForm(instance=viewed_user, initial={'email_subscribe': email_subscribe_initial},
                               user_role=current_user.details.role)

    actions = Action.objects.filter(user=viewed_user).order_by('-created')[:5]
    return render(request, "users/user/profile.html",
                  {"current_user": current_user, "viewed_user": viewed_user, "actions": actions, "form": form,
                   "editable": editable})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username have existed
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username '%s' is already taken. Please choose a different one." % username)
            return render(request, "users/user/register.html")

        user = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['role'] = user.details.role
            messages.success(request, "You successfully registered and logged in with the username: %s" % user.username)
            return redirect('truthtaste:all_restaurant_list')
        else:
            messages.error(request, "Automatic login failed. Please try to log in manually.")
            return redirect('truthtaste:home')
    else:
        return render(request,
                      "users/user/register.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['role'] = user.details.role
            messages.success(request, 'Successfully logged in!')
            return redirect('truthtaste:all_restaurant_list')
        else:
            messages.error(request, 'Invalid user name or password.')
            return redirect('users:log-in-page')

    return render(request, "truthtaste/auth/log-in-page.html")


def logout(request):
    del request.session['username']
    del request.session['role']
    return redirect('truthtaste:home')
