from django.contrib.auth.views import LogoutView
from django.urls import path
from core import views

urlpatterns = [
    path('index/', views.rend_index, name='index'),
    path('dashboard/', views.dash_view, name='dashboard'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(template_name='modals/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]