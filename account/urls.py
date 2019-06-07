from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),

    path('users/follow/', views.user_follow, name='user_follow'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('', views.HomeView, name='index'),
]

# Problem
# password_change works but a problem redirecting to password_change_done.  Error is -> "django.urls.exceptions.NoReverseMatch: Reverse for 'password_change_done' not found. 'password_change_done' is not a valid view function or pattern name."
# password reset has same issue
# -> "django.urls.exceptions.NoReverseMatch: Reverse for 'password_reset_done' not found. 'password_reset_done' is not a valid view function or pattern name."
# -> "django.urls.exceptions.NoReverseMatch: Reverse for 'password_reset_complete' not found. 'password_reset_complete' is not a valid view function or pattern name."
# SOLUTION: The code that is reversing (password_reset_done, password_reset_complete, password_change_done) doesn't expect you to be using a namespace. The simplest solution is to remove "app_name" and namespace from the urls.py files or move the password_reset URL patterns to a different urls.py that doesn't set app_name
# if you must use the namespace, then you'll need to change the view/template to use the app's namespace wherever you reverse the URLS.