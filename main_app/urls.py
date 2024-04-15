from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='delete_post'),
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:profile_id>/add_photo/', views.add_user_photo, name='add_user_photo'),
    path('profiles/<int:profile_id>/follow/', views.follow_profile, name='follow_profile'),
    path('profiles/<int:profile_id>/unfollow/', views.unfollow_profile, name='unfollow_profile'),
]
