from django.urls import include, path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from assets.views import PropertyViewSet, ContractViewSet, DepartmentViewSet, CategoryViewSet
from contacts.views import SupplierViewSet
from core.views import UserViewSet
from maintenance.views import MaintenanceViewSet
from movements.views import MovementViewSet

router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r'contracts', ContractViewSet)
router.register(r"Department",DepartmentViewSet)
router.register(r'Categories', CategoryViewSet)
router.register(r'User',UserViewSet)
router.register(r'Suplier',SupplierViewSet)
router.register(r'Maintenance',MaintenanceViewSet)
router.register(r'Movements',MovementViewSet)
urlpatterns = router.urls


