from django.shortcuts import render
from .models import Post
# Create your views here.


def home(request):
    return render(request, 'home.html')

def post_index(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {
        'posts': posts
    })