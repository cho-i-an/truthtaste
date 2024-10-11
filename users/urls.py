from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('auth/log-in-page', views.login_page, name='log-in-page'),
    path('logout', views.logout, name='logout'),
]

