from django.shortcuts import render, redirect
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, PostForm
# Create your views here.


def home(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:  # Check if user is logged in
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.profile = request.user.profile
                post.save()
                return redirect('home')
        else:
            form = PostForm()
        return render(request, 'home.html', {'form': form, 'posts': posts})
    else:
        return render(request, 'home.html', {'posts': posts})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid signup'
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html', {
        'error_message': error_message,
        'user_form': user_form,
        'profile_form': profile_form
    })
