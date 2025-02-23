from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('list-maintenance/', MaintenanceListView.as_view(), name='list-maintenance'),
    path('create-maintenance/', MaintenanceCreateView.as_view(), name='create-maintenance'),
    path('<int:pk>/update-maintenance/',MaintenanceUpdateView.as_view(), name = 'update-maintenance'),
    path('<int:pk>/admin-update-maintenance/',AdminMaintenanceUpdateView.as_view(), name = 'admin-update-maintenance'),
    path('<int:pk>/maintenance-confirm-delete/',MaintenanceDeleteView.as_view(), name = 'maintenance-confirm-delete'),
]
