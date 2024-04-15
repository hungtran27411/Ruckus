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
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('following/', views.following_page, name='following_page')
]   
