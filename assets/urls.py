from graphene_django.views import GraphQLView
from .views import *
from django.urls import path
from . import views
from config.schema import schema

# URLs do app assets

urlpatterns = [
    # URLs relacionadas a Contratos
    path('list-contracts/', list_contracts, name='list-contracts'),
    path('create-contracts/', ContractCreateView.as_view(), name='create-contracts'),
    path('<int:pk>/update-contract/', ContractUpdateView.as_view(), name='update-contract'),
    path('<int:pk>/contract-confirm-delete/', ContractDeleteView.as_view(), name='contract-confirm-delete'),

    # URLs relacionadas a Categorias
    path('list-category/', views.list_category, name='list-category'),
    path('create-category/', CategoryCreateView.as_view(), name='create-category'),
    path('<int:pk>/update-category/', CategoryUpdateView.as_view(), name='update-category'),
    path('<int:pk>/category-confirm-delete/', CategoryDeleteView.as_view(), name='category-confirm-delete'),

    # URLs relacionadas a Departamentos
    path('list-department/', views.list_department, name='list-department'),
    path('create-department/', DepartmentCreateView.as_view(), name='create-department'),
    path('<int:pk>/update-department/', DepartmentUpdateView.as_view(), name='update-department'),
    path('<int:pk>/department-confirm-delete/', DepartmentDeleteView.as_view(), name='department-confirm-delete'),

    # URLs relacionadas a Propriedades
    path('list-property/', views.index, name='list-property'),
    path('create-property/', PropertyCreateView.as_view(), name='create-property'),
    path('<int:pk>/admin-update-property/', AdminPropertyUpdateView.as_view(), name='admin-update-property'),
    path('<int:pk>/update-property/', PropertyUpdateView.as_view(), name='update-property'),
    path('<int:pk>/property-confirm-delete/', PropertyDeleteView.as_view(), name='property-confirm-delete'),

    # URL para GraphQL
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]