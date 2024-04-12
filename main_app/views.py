from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, PostForm
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.module_loading import import_string
# Create your views here.


def home(request):
    posts = Post.objects.order_by('-id')  # Retrieve posts in reverse chronological order based on id
    if request.user.is_authenticated:  
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
            error_message = 'Invalid sign up.  Please check your information and try again.'
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    
    help_texts = get_password_validators_help_texts()
    return render(request, 'registration/signup.html', {
        'error_message': error_message,
        'user_form': user_form,
        'profile_form': profile_form,
        'help_texts': help_texts
    })


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'edit.html'

    success_url = '/'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'edit.html'
    success_url = '/'


def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    posts = Post.objects.filter(profile=profile)
    return render(request, 'profile/profile.html', {
        'profile': profile,
        'posts': posts,
    })

def get_password_validators_help_texts():
    validators = settings.AUTH_PASSWORD_VALIDATORS
    help_texts = []
    for validator_config in validators:
        ValidatorClass = import_string(validator_config['NAME'])
        validator = ValidatorClass()
        help_texts.append(validator.get_help_text())
    return help_texts