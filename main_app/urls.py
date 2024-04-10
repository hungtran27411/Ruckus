from django.urls import path
from . import views 

urlpatterns = [
    path('', views.post_index, name='home'),
    path('accounts/singup/', views.signup, name='signup')
]