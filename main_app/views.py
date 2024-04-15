from django.shortcuts import render, redirect
from .models import Post, Profile, Photo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, PostForm
from django.urls import reverse_lazy, reverse
# stuff for photo upload for aws
import uuid # for random numbers (used in generating photo name)
import boto3 # aws sdk that lets us talk to our s3 bucket
import os # this lets us talk to the .env
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import HttpResponseNotAllowed
# Create your views here.


def home(request):
    posts = Post.objects.order_by('-id')  # Retrieve posts in reverse chronological order based on id
    profile = None  # Initialize profile variable
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
            profile = request.user.profile  # Retrieve the user's profile
        return render(request, 'home.html', {'form': form, 'posts': posts, 'profile': profile})
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
    print(profile)
    return render(request, 'profile/profile.html', {
        'profile': profile,
        'posts': posts,
        # add photos : photos?
    })

def add_user_photo(request, profile_id):
    # profile = request.user.profile
    photo_file = request.FILES.get('photo-file', None)
    
    if photo_file:
        s3 = boto3.client('s3')
        key = 'profile_photos/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, profile_id=profile_id) # i thought the object was created here similar to catcollector
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    # profile_page_url = reverse('profile_detail', kwargs={'profile_id': request.user.profile.id})
    
    # Redirect to the profile page URL
    return redirect('profile_detail', profile_id=profile_id)
    

def get_password_validators_help_texts():
    validators = settings.AUTH_PASSWORD_VALIDATORS
    help_texts = []
    for validator_config in validators:
        ValidatorClass = import_string(validator_config['NAME'])
        validator = ValidatorClass()
        help_texts.append(validator.get_help_text())
    return help_texts

@login_required
def follow_profile(request, profile_id):
    if request.method == 'POST':
        profile_to_follow = Profile.objects.get(id=profile_id)
        request.user.profile.following.add(profile_to_follow)
        return redirect('profile_detail', profile_id=profile_id)
    else: 
        return HttpResponseNotAllowed(['POST'])
    
@login_required
def unfollow_profile(request, profile_id):
    if request.method == 'POST':
        profile_to_unfollow = Profile.objects.get(id=profile_id)
        request.user.profile.following.remove(profile_to_unfollow)
        return redirect('profile_detail', profile_id=profile_id)
    else:
        
        return HttpResponseNotAllowed(['POST'])