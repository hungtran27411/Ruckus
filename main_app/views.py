from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
	return render(request, 'home.html')


def post_index(request):
	posts = Post.objects.all()
	return render(request, 'home.html', {
		'posts': posts
	})


def signup(request):
	error_message = ''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')
		else:
			error_message = 'Invalid signup'
	form = UserCreationForm()
	return render(request, 'registration/signup.html', {
		'error_message': error_message,
		'form': form
	})


class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['content']

	def form_valid(self, form):
		
		form.instance.user = self.request.user
		
		return super().form_valid(form)
		
	