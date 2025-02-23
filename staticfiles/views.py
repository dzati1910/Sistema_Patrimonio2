import core.dash_app
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer
from assets.models import *
from .forms import PropertyForm
class UserViewSet(viewsets.ModelViewSet):
    """
    Criação de um novo usuário (API RESTful)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

def index(request):
    """Renderiza a página inicial do sistema"""
    properties = Property.objects.all()
    form = PropertyForm()
    return render(request, 'list-property.html', {'properties': properties})

def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to your home page
    else:
        form = PropertyForm()
    return render(request, 'modals/create_property.html', {'form': form})

def rend_index(request):
    return render(request,'index.html')


import requests
from django.shortcuts import render


def dash_view(request):
    return render(request, 'dash_template.html')
