from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name="main"),
    path('auth/', views.auth, name="auth"),
    path('logout/', views.logout_twitter, name="logout"),
    path('connected/', views.connected),
    path('profile/', views.profile, name="profile"),
    path('permission_tweet/', views.permission_tweet, name="perm"),
    path('delete_permission/', views.delete_permission, name="del_perm"),
    path('tweet/', views.tweet, name="tweet"),
    path('form_tweet/', views.form_tweet),
]