from django.urls import path
from . import views

urlpatterns = [
    path('list-property/', views.index, name='list-property'),  # Mapeia http://localhost:8000/ para list-property.html
    path('create-property/', views.create_property, name='create-property'),
    path('index/',views.rend_index,name= 'index'),
    path('dashboard/', views.dash_view, name='dashboard'),
]