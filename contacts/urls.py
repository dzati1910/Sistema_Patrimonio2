# contacts/urls.py
from django.urls import path
from . import views
from .views import *

# URLs do app contacts

urlpatterns = [
    # Listar todos os fornecedores
    path('list-contacts/', views.list_contacts, name='list-contacts'),

    # Criar um novo fornecedor
    path('create-contacts/', SupplierCreateView.as_view(), name='create-contacts'),

    # Atualizar um fornecedor existente
    path('<int:pk>/update-contacts/', SupplierUpdateView.as_view(), name='update-contacts'),

    # Excluir um fornecedor existente
    path('<int:pk>/supplier-confirm-delete/', SupplierDeleteView.as_view(), name='supplier-confirm-delete'),
]