from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signup, name='signup'),  # Default path directs to the signup page
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('send_message/', views.send_message, name='send_message'),
]