from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('list-movement/',views.list_movement, name = 'list-movement'),
    path('create-movement/', MovementCreateView.as_view(), name='create-movement'),
    path('<int:pk>/update-movement/',MovementUpdateView.as_view(), name = 'update-movement'),
    path('<int:pk>/movement-confirm-delete/',MovementDeleteView.as_view(), name = 'movement-confirm-delete'),
]